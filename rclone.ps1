Set-Location "C:\Programs\rclone\"
taskkill /F /IM rclone.exe
.\rclone.exe mount Alist:/ Z: --vfs-cache-mode full --cache-dir C:/Programs/rclone/Temp
