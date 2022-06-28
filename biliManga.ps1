$paraUrl = "https://manga.bilibili.com/mc28173/454790"
$chromeArgument = "--new-window"
$runProgram = "`"C:\Program Files\CentBrowser\Application\chrome.exe`""
$matchString = "哔哩哔哩漫画"

echo $startString
Start-Process -FilePath $runProgram -ArgumentList $paraUrl, $chromeArgument
Start-Sleep -Seconds 5
$title = Get-Process | Where-Object { $_.mainWindowTitle } | format-table id, mainwindowtitle | Out-String
$title = $title -split "`r`n"

foreach ($line in $title) {
    if ($line.contains($matchString)) {
        $killPid = $line -split (' ')
        $killPid = $killpid[0]
        Write-Output $killPid
        #gsudo Stop-Process -Id $killPid
    }
}
