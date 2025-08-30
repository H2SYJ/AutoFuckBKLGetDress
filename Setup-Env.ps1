# �������⻷������
$venvName = "venv"

# ��� Python �Ƿ�װ
try {
    python --version 2>&1 | Out-Null
} catch {
    Write-Error "δ�ҵ� Python ���������Ȱ�װ Python ����ӵ�ϵͳ PATH"
    pause
    exit 1
}

# ��� requirements.txt �Ƿ����
if (-not (Test-Path "requirements.txt")) {
    Write-Error "��ǰĿ¼δ�ҵ� requirements.txt �ļ�"
    pause
    exit 1
}

# �������⻷��
Write-Host "���ڴ������⻷�� $venvName..."
python -m venv $venvName

if (-not (Test-Path "$venvName\Scripts\Activate.ps1")) {
    Write-Error "���⻷������ʧ��"
    pause
    exit 1
}

# �������⻷������װ����
Write-Host "���ڰ�װ������..."
& "$venvName\Scripts\Activate.ps1"

# ��װ����
pip install -r requirements.txt

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
    