@echo off
cd /d "%~dp0"
rem Offers unfinished runs first, then channel, count, and the nine AI choices.
".venv\Scripts\python.exe" make_shorts.py
pause
