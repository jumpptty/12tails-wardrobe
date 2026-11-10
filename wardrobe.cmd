@echo off
rem 12 Tails wardrobe: a local server for the project folder, then the page (pipeline/wardrobe_data.py builds its data).
rem The server closes itself about 10 s after the last wardrobe page closes (pipeline/wardrobe_serve.py)
cd /d "%~dp0"
start "wardrobe server" /min py -3 pipeline\wardrobe_serve.py 8771
timeout /t 2 /nobreak >nul
start "" http://127.0.0.1:8771/wardrobe/
