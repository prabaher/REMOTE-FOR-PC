@echo off
title Laptop Remote V2

cd /d "%~dp0"

echo ==========================================
echo          LAPTOP REMOTE V2
echo ==========================================
echo.

for /f "delims=" %%I in ('powershell -NoProfile -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' -and $_.PrefixOrigin -ne 'WellKnown'} | Select-Object -First 1 -ExpandProperty IPAddress)"') do set "IP=%%I"

echo Laptop IP:
echo %IP%
echo.

echo Phone URL:
echo http://%IP%:5000
echo.

echo Local URL:
echo http://127.0.0.1:5000
echo.

echo Starting server...
echo Keep this window open while using the remote.
echo ==========================================
echo.

start "" /b cmd /c "timeout /t 2 /nobreak >nul & start http://127.0.0.1:5000"

python app.py

pause