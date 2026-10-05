@echo off
title Laptop Remote V2

cd /d "%~dp0"

echo ==========================================
echo          LAPTOP REMOTE V2
echo ==========================================
echo.

for /f "delims=" %%I in ('powershell -NoProfile -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' -and $_.PrefixOrigin -ne 'WellKnown'} | Select-Object -First 1 -ExpandProperty IPAddress)"') do set "IP=%%I"

echo Laptop IP: %IP%
echo.

python generate_qr.py "%IP%"

echo Starting Flask server...
echo Keep this window open while using the remote.
echo.

python app.py

pause