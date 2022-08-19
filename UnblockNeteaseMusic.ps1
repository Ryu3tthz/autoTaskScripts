Set-Location "~\Documents\GitHub\server"
forever stopall
forever start .\app.js -p 19888:19889