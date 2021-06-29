@echo off
cls
adb logcat -c
adb logcat -G 256m
adb logcat -b all