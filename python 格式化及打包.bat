@ECHO OFF
CLS
TITLE Python �榡��(�ϥ�Black�M��)
COLOR F0

:ShowList
ECHO.
ECHO ==============================================
ECHO ��e�ؿ��U�Ҧ� Python ���:
ECHO.
dir /B /O:S /A-d *.py
GOTO Ask


:Ask
ECHO.
ECHO ==============================================
set /p Ask="�п�J�ɮצW��:"
ECHO.
ECHO �n�榡�ƪ����:%Ask%
ECHO.
CHOICE /C YN /N /M "�O�_�i��榡�ƤΥ��]�Ϋ�N��^(Y/N):"
IF ERRORLEVEL 2 (
 GOTO END2
)ELSE IF ERRORLEVEL 1 (  
 GOTO Format
)


:Format
ECHO.
ECHO ==============================================
ECHO [1/2] �i��榡��...
ECHO.
black %Ask%
if %errorlevel% NEQ 0 (GOTO Fail-Format)ELSE (GOTO Package)


:Package
ECHO.
ECHO ==============================================
ECHO [2/2] �i�楴�]...
ECHO.
pyinstaller -F %Ask% -c --icon=icon.ico
if %errorlevel% NEQ 0 (GOTO Fail-Package)ELSE (GOTO END1)


:Fail-Format
ECHO.
ECHO ==============================================
CLS
ECHO.
ECHO �榡�ƥ��ѡA���ˬdPython�ɮפ��e�O�_���~
GOTO ShowList


:Fail-Package
ECHO.
ECHO ==============================================
CLS
ECHO.
ECHO ���]���ѡA���ˬdPython�ɦW��ICON�ϼЦW�٬O�_���~
GOTO ShowList


:END1
ECHO.
ECHO ==============================================
ECHO �榡�ƤΥ��]���\!
ECHO.
PAUSE...
EXIT

:END2
CLS
GOTO ShowList