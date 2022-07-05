$chromeArgument = "--new-window"
$urls = @("https://manga.bilibili.com/mc28173/454790", "https://www.pttime.org/attendance.php")
$filePath = "`"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe`""
foreach ($url in $urls) {
    Start-Process  -ArgumentList $url, $chromeArgument -WindowStyle Minimized -FilePath $filePath
}
Start-Sleep -Seconds 5
Stop-Process -Name "msedge"