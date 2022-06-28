@REM @echo off
cd "C:\Users\primi\Documents\GitHub\ArknightsAutoHelper\"
@REM echo "Please wait..."
@REM timeout /t 16
@REM adb connect localhost:62001
@REM adb shell am start -n com.hypergryph.arknights.bilibili/com.u8.sdk.SplashActivity
@REM timeout /t 14
@REM adb shell input tap 500 500
@REM timeout /t 18
@REM akhelper.py c
@REM timeout /t 1
@REM adb shell input tap 106 36
@REM timeout /t 1
@REM adb shell input tap 1094 189
python akhelper.py