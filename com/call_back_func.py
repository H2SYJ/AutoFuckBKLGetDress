import time
from datetime import datetime
from threading import Thread
import cv2
from pynput.keyboard import Key
import global_config
from pynput import keyboard
from util.util import print_log


def leave_team():
    print_log(f"开始执行退队逻辑,from {global_config.global_status} to 4")
    global_config.global_status = 4
    keyboard_controller = keyboard.Controller()
    keyboard_controller.press(Key.esc)
    time.sleep(0.2)
    keyboard_controller.release(Key.esc)
    time.sleep(1)
    keyboard_controller.press("i")
    time.sleep(0.2)
    keyboard_controller.release("i")
    #
    time.sleep(1)
    global_config.automation_tool.click_position(1764, 971)
    time.sleep(1)
    global_config.automation_tool.click_position(1192, 766)
    time.sleep(1)
    for i in range(3):
        keyboard_controller.press(Key.esc)
        time.sleep(0.2)
        keyboard_controller.release(Key.esc)
    press_f()
    print_log(f"执行退队逻辑结束,from {global_config.global_status} to 0")
    global_config.global_status = 0


def press_f():
    print_log("点击F")
    keyboard_controller = keyboard.Controller()
    keyboard_controller.press('f')
    time.sleep(0.2)
    keyboard_controller.release('f')


def change_to_outer_fb():
    print_log(f"已在副本外部，global_status from {global_config.global_status} to 0")
    global_config.global_status = 0


def begin_fb_loop():
    if global_config.target_careers is not None and global_config.red_careers is not None:
        switch_careers(global_config.target_careers)
    if global_config.global_status == 1 or global_config.global_status == 0:
        print_log(f"启动键盘回放,global_status from {global_config.global_status} to 2")
        global_config.replay.start_replay(global_config.script_json)
        global_config.global_status = 2
        global_config.fb_times = global_config.fb_times + 1
        global_config.last_fb_start_time = time.time()
        Thread(target=_time_out, args=(), daemon=True).start()


def checkBoss():
    check_boss_name = global_config.automation_tool.ocr_check(600, 20, 700, 100)
    for str, _ in check_boss_name:
        if "伊" in str or "罗" in str or "蒂娜" in str or "勇士" in str or "特" in str or "丹" in str:
            return True
    return False


def _time_out():
    fb_times = global_config.fb_times
    begin = time.time()
    print_log(f"启动超时检测线程，当前为第{fb_times}次副本攻略,共计超时{global_config.fb_time_out_times}次，开启时间为：{datetime.now()}")
    while time.time() - begin < global_config.fb_time_out_sec and fb_times == global_config.fb_times:
        if global_config.global_status == 5:
            print_log("人物发生死亡，需退出副本重新进入")
            time.sleep(10)
            _confirm_time_out_reason()
            return
        if global_config.replay.replaying == False:
            time.sleep(8)
            if not checkBoss():
                print_log("录制结束，但未进入BOSS阶段，强制超时退出")
                break
            else:
                print_log(f"录制结束，成功进入BOSS阶段，退出超时检测线程")
                return
        time.sleep(1)
    if global_config.global_status == 2 and fb_times == global_config.fb_times:
        curr_time = time.time()
        global_config.fb_time_out_times = global_config.fb_time_out_times + 1
        print_log(
            f"超时退出副本,共计超时{global_config.fb_time_out_times}次,保存超时时的截图game_time_out_{curr_time}.png,global_status from {global_config.global_status} to 4")

        global_config.global_status = 4
        try:
            img = global_config.automation_tool.capture_game_window()
            cv2.imwrite(f"game_time_out_{curr_time}.png", img)
        except Exception as e:
            print_log(e)
        _confirm_time_out_reason()
    else:
        print_log("未超时，超时检测线程退出")


def _confirm_time_out_reason():
    print_log("开始校验超时原因")
    has_error = False
    keyboard_controller = keyboard.Controller()
    print_log("开始校验月卡")
    global_check = global_config.automation_tool.ocr_check()
    print_log("开始校验死亡")
    for str, _ in global_check:
        if "复活" in str:
            print_log("确认为死亡导致的超时")
            has_error = True
            global_config.automation_tool.click_position(1696, 948)
            time.sleep(5)

    for str, _ in global_check:
        if "典藏卡" in str or "空白" in str:
            print_log("确认为月卡导致的超时")
            has_error = True
            for i in range(2):
                global_config.automation_tool.click_position(1349, 552)
                time.sleep(0.5)
            keyboard_controller.press(Key.esc)
            time.sleep(0.2)
            keyboard_controller.release(Key.esc)
    print_log("开始校验路径错误")
    is_in_fb = global_config.automation_tool.ocr_check(*global_config.ocr_info_arr["副本内"].pos)
    for str, _ in is_in_fb:
        if global_config.ocr_info_arr["副本内"].match_str in str:
            print_log("确认为路径错误导致的超时")
            has_error = True
            # 退出副本
            keyboard_controller.press("p")
            time.sleep(0.2)
            keyboard_controller.release("p")
            #
            time.sleep(1)
            global_config.automation_tool.click_position(1192, 770)
    # TODO 断线重连
    print_log("开始校验掉线")
    for str, _ in global_check:
        if "断开连接" in str:
            print_log("确认为断开连接")
            has_error = True
            global_config.automation_tool.click_position(958, 800)
            time.sleep(20)
            global_config.automation_tool.click_position(958, 913)
            time.sleep(1)
            global_config.automation_tool.click_position(958, 913)
            time.sleep(20)
            global_config.automation_tool.click_position(1660, 950)
            time.sleep(1)
            global_config.automation_tool.click_position(1660, 950)
            time.sleep(20)
    if has_error:
        time.sleep(3)
        print_log("再次校验超时原因")
        _confirm_time_out_reason()
    else:
        print_log(f"校验超时原因结束，global_status from {global_config.global_status} to 2")
        global_config.global_status = 2


def global_error_check():
    time_out = 11 * 60
    while True:
        try:
            if time.time() - global_config.last_fb_start_time > time_out:
                print_log(
                    f"距离上一次（{global_config.last_fb_start_time}）进入副本已经超过{time_out}秒，开始执行全局异常检测")

                # 上一次进入副本到现在过去了15分钟，开启全局异常检测
                global_config.global_status = 4
                _confirm_time_out_reason()
            time.sleep(120)
        except Exception as e:
            print(e)


def pre_operation_check():
    while True:
        try:
            if global_config.global_status==0:
                change_to_20_team(0)
                if global_config.target_careers is not None and global_config.red_careers is not None:
                    switch_careers(global_config.red_careers)
                print_log(f"20人队伍创建完成,global_status from {global_config.global_status} to 1")
                global_config.global_status = 1
            time.sleep(2)
        except Exception as e:
            print(e)

def switch_careers(careers_name):
    print("目标职业"+careers_name)
    keyboard_controller = keyboard.Controller()
    keyboard_controller.press("c")
    time.sleep(0.3)
    keyboard_controller.release("c")
    time.sleep(1)
    global_config.automation_tool.click_position(1200, 430)
    time.sleep(1)
    careers_list = global_config.automation_tool.ocr_check(0,100,280,950)
    for str, pos in careers_list:
        print(str, pos)
        if careers_name in str:
            x,y,w,h = pos
            for i in range(3):
                global_config.automation_tool.click_position(x + w / 2, y + h / 2,is_abs_pos=True)
                time.sleep(0.3)
            break
    global_config.automation_tool.click_position(1750, 950)
    time.sleep(1)
    global_config.automation_tool.click_position(1200, 800)
    time.sleep(1)
    global_config.automation_tool.click_position(1200, 800)
    time.sleep(1)
    global_config.automation_tool.click_position(1164, 1017)
    time.sleep(1)
    for i in range(3):
        time.sleep(1)
        keyboard_controller.press(Key.esc)
        time.sleep(0.3)
        keyboard_controller.release(Key.esc)

def change_to_20_team(retry_times):
    time.sleep(1)
    # if retry_times > 2:
    #     print_log(f"创建20人队伍失败,global_status from {global_config.global_status} to 1")
    #     global_config.global_status = 1
    keyboard_controller = keyboard.Controller()
    # 进入组队页面
    keyboard_controller.press("i")
    time.sleep(0.3)
    keyboard_controller.release("i")
    # 点击创建队伍
    time.sleep(1)
    global_config.automation_tool.click_position(1720, 990)
    time.sleep(1)
    # 点击变为20人队伍
    global_config.automation_tool.click_position(1108, 993)
    time.sleep(1)

    keyboard_controller.press(Key.esc)
    time.sleep(0.3)
    keyboard_controller.release(Key.esc)
    time.sleep(1)
    # is_success = False
    # # 校验是否已经创建20人队伍
    # team_ocr = global_config.automation_tool.ocr_check(1462,200,250,100)
    # for str, _ in team_ocr:
    #     if "队" in str:
    #         is_success = True
    # if is_success:
    #     print_log(f"20人队伍创建完成,global_status from {global_config.global_status} to 1")
    #     global_config.gwslobal_status = 1
    # else:
    #     change_to_20_team(retry_times+1)


def press_esc(x,y,w,h):
    keyboard_controller = keyboard.Controller()
    keyboard_controller.press(Key.esc)
    time.sleep(0.3)
    keyboard_controller.release(Key.esc)
    return 0,0