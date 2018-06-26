@echo off 
adb wait-for-device

adb push \\172.17.30.81\root\CQA83TAndroid_v2.1.0_bv3\lichee\out\sun8iw6p1\android\common\lib\modules\3.4.39\ts.ko /sdcard/
adb push \\172.17.30.81\root\CQA83TAndroid_v2.1.0_bv3\lichee\out\sun8iw6p1\android\common\lib\modules\3.4.39\disp.ko /sdcard/

adb remount
adb shell cp /sdcard/ts.ko /system/vendor/modules/ts.ko
adb shell cp /sdcard/disp.ko /system/vendor/modules/disp.ko

adb shell chmod 644 /system/vendor/modules/ts.ko
adb shell chmod 644 /system/vendor/modules/disp.ko

adb reboot

pause
