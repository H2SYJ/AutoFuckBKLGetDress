$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
if (-not $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Host "`n��Ҫ����ԱȨ�޲��ܼ����������� UAC ��ʾ..." -ForegroundColor Cyan
    Write-Host "��ʾ��ԭ���ڽ��� 2 ���رգ��¹���Ա���ڻ�����" -ForegroundColor Cyan
    Start-Sleep -Seconds 1  # �ȴ�1 �룬���û�������ʾ
    
    $arguments = "-File `"$($MyInvocation.MyCommand.Definition)`""
    Start-Process powershell.exe -Verb RunAs -ArgumentList $arguments
    exit
}

# �����ǹ���ԱȨ�޵ĺ����߼�
Write-Host "`n? �ѻ�ȡ����ԱȨ�ޣ���ʼִ�в���..." -ForegroundColor Green
# ����ĺ��Ĵ��룬���紴�����⻷������װ�����ȣ�
$scriptPath = $PSScriptRoot
Write-Host "��ǰ�ű�Ŀ¼: $scriptPath"

# ƴ�����⻷����Python�ľ���·��
$pythonPath = Join-Path -Path $scriptPath -ChildPath "venv\Scripts\python.exe"
# ƴ��Main.py�ľ���·��
$mainScript = Join-Path -Path $scriptPath -ChildPath "com\recorder.py"
& $pythonPath $mainScript
# ��������ͣ������ִ����ֱ�ӹر�
Write-Host "`n? ������ɣ�" -ForegroundColor Green
pause


pause