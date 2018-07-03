@echo off
adb wait-for-device
echo Android Monitoring...
adb shell logcat >> %1\logcat.txt