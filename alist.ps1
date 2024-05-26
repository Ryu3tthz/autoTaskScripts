Set-Location "C:\Programs\alist\"
$processName = "alist"
$process = Get-Process -Name $processName -ErrorAction SilentlyContinue
if ($process) {
    $process | Stop-Process -Force
}
.\alist.exe server
start-sleep -s 5
Set-Location "C:\Programs\rclone\"
$processName = "rclone"
$process = Get-Process -Name $processName -ErrorAction SilentlyContinue
if ($process) {
    $process | Stop-Process -Force
}
.\rclone.exe mount Alist:/ Z: --vfs-cache-mode full --cache-dir C:/Programs/rclone/Temp  --network-mode