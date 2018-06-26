@echo off

set "TO_NUL= >NUL 2>NUL"
set DEBUG=0
set "PROJECT=MyProject"

if "%1" == "cmd" (
	@echo on
	set DEBUG=1
	set "TO_NUL="
) 

echo Wait for device...
adb wait-for-device

if "%time:~0,1%" == " " (
	set "test_dir=%PROJECT%_%date:~0,4%%date:~5,2%%date:~8,2%_0%time:~1,1%%time:~3,2%"
) else (
	set "test_dir=%PROJECT%_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%"
)
echo Log Saved in: %test_dir%
if exist %test_dir%  rd /s /q %test_dir% %TO_NUL%
mkdir %test_dir% %TO_NUL%

adb shell cat /proc/last_kmsg > %test_dir%\last_dmsg.txt
adb shell dmesg > %test_dir%\dmesg.txt
adb logcat -d > %test_dir%\logcat.txt

pause