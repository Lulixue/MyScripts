@echo off
adb wait-for-device
echo Kernel Monitoring...
adb shell cat /proc/kmsg >> %1\\kmsg.txt
