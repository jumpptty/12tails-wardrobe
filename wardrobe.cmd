@echo off
rem 12 Tails wardrobe: a local server for the project folder, then the page (pipeline/wardrobe_data.py builds its data)
cd /d "%~dp0"
start "wardrobe server" /min py -3 -m http.server 8771 --bind 127.0.0.1
timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:8771/wardrobe/
