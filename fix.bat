@echo off
cd /d "%~dp0"
rem Re-renders one scene of a Short made in the last 7 days (same pictures, voice and music).
".venv\Scripts\python.exe" make_shorts.py fix
pause
