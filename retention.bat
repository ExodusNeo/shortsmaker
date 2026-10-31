@echo off
cd /d "%~dp0"
rem Match a YouTube Studio retention screenshot to a finished Short's scenes.
".venv\Scripts\python.exe" make_shorts.py retention %*
pause
