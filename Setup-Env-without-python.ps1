# �������⻷������
$venvName = "venv"
mv ./venv_back ./venv
# �������⻷������װ����
Write-Host "���ڰ�װ������..."
& "$venvName\Scripts\Activate.ps1"

# ��װ����
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

if ($LASTEXITCODE -ne 0) {
    Write-Error "��������װʧ��"
    pause
    exit 1
}

# �˳����⻷��
deactivate

Write-Host "`n����������ɣ�"
Write-Host "�������⻷�������.\\$venvName\Scripts\Activate.ps1"
pause
    