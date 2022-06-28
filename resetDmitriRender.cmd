reg delete HKEY_CURRENT_USER\SOFTWARE\DmitriRender /f
cd /d %USERPROFILE%\Documents

set data1=[{
set data2=Class
set data3=RunTimeData
for /f "delims=" %%a in ('findstr /b /i /v /c:"%data1%" "desktop.ini"') do (
echo %%a>>file.ini
)
move /y file.ini desktop.ini
for /f "delims=" %%a in ('findstr /b /i /v /c:"%data2%" "desktop.ini"') do (
echo %%a>>file.ini
)
move /y file.ini desktop.ini
for /f "delims=" %%a in ('findstr /b /i /v /c:"%data3%" "desktop.ini"') do (
echo %%a>>file.ini
)
move /y file.ini desktop.ini
attrib +s +h desktop.ini