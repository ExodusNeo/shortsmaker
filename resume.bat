@echo off
cd /d "%~dp0"
rem Continue unfinished Shorts from their last completed stage.
".venv\Scripts\python.exe" make_shorts.py resume %*
pause
