Set-Location "C:\Programs\rclone\"
$processName = "rclone.exe"
$process = Get-Process -Name $processName -ErrorAction SilentlyContinue
if ($process) {
    $process | Stop-Process -Force
}
.\rclone.exe mount Alist:/ Z: --vfs-cache-mode full --cache-dir C:/Programs/rclone/Temp  --network-mode