from rapidocr_onnxruntime import RapidOCR
import cv2
import numpy as np
from PIL import Image

# 初始化RapidOCR引擎
# 可以通过lang_list参数指定语言，对于数字识别可以只保留英文
rapid_ocr = RapidOCR(
    lang_list=['en']  # 只使用英文模型，更适合数字识别
)

def recognize_numbers(image_path):
    """
    识别图像中的数字
    """
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"无法读取图像: {image_path}")
    
    # 进行OCR识别
    result, elapse = rapid_ocr(image)
    print(result)
    
    return result, elapse

# 使用示例
if __name__ == "__main__":
    image_path = "F:/.Projects/AutoFuckBKLGetDress/com/1758800433.002547.png"  # 替换为你的图像路径
    recognize_numbers(image_path)