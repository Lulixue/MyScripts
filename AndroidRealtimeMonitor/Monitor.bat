@echo off

set "TO_NUL= >NUL 2>NUL"
set DEBUG=0

if "%1" == "cmd" (
	@echo on
	set DEBUG=1
	set "TO_NUL="
) 

echo Wait for device...
adb wait-for-device

if "%time:~0,1%" == " " (
	set "test_dir=MonitorLog_%date:~0,4%%date:~5,2%%date:~8,2%_0%time:~1,1%%time:~3,2%"
) else (
	set "test_dir=MonitorLog_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%"
)
echo Log Tracing in: %test_dir%
if exist %test_dir%  rd /s /q %test_dir% %TO_NUL%
mkdir %test_dir% %TO_NUL%

start /min cmd /c MonitorKernel.bat  %test_dir% 
call MonitorAndroid.bat %test_dir%
REM start /min cmd /c MonitorKernel.bat  %test_dir%

pause