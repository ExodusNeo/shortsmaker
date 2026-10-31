@echo off
cd /d "%~dp0"
rem Asks channel, count, then 3 solo AIs or any of the 6 writer/editor pairings.
".venv\Scripts\python.exe" make_shorts.py
pause
