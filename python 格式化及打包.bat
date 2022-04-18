@ECHO OFF
CLS
TITLE Python 格式化(使用Black套件)
COLOR F0

:ShowList
ECHO.
ECHO ==============================================
ECHO 當前目錄下所有 Python 文件:
ECHO.
dir /B /O:S /A-d *.py
GOTO Ask


:Ask
ECHO.
ECHO ==============================================
set /p Ask="請輸入檔案名稱:"
ECHO.
ECHO 要格式化的文件:%Ask%
ECHO.
CHOICE /C YN /N /M "是否進行格式化及打包或按N返回(Y/N):"
IF ERRORLEVEL 2 (
 GOTO END2
)ELSE IF ERRORLEVEL 1 (  
 GOTO Format
)


:Format
ECHO.
ECHO ==============================================
ECHO [1/2] 進行格式化...
ECHO.
black %Ask%
if %errorlevel% NEQ 0 (GOTO Fail-Format)ELSE (GOTO Package)


:Package
ECHO.
ECHO ==============================================
ECHO [2/2] 進行打包...
ECHO.
pyinstaller -F %Ask% -c --icon=icon.ico
if %errorlevel% NEQ 0 (GOTO Fail-Package)ELSE (GOTO END1)


:Fail-Format
ECHO.
ECHO ==============================================
CLS
ECHO.
ECHO 格式化失敗，請檢查Python檔案內容是否有誤
GOTO ShowList


:Fail-Package
ECHO.
ECHO ==============================================
CLS
ECHO.
ECHO 打包失敗，請檢查Python檔名或ICON圖標名稱是否有誤
GOTO ShowList


:END1
ECHO.
ECHO ==============================================
ECHO 格式化及打包成功!
ECHO.
PAUSE...
EXIT

:END2
CLS
GOTO ShowList