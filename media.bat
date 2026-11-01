@echo off
cd /d "%~dp0"
".venv\Scripts\python.exe" make_shorts.py media
pause
