@echo off
cd /d "%~dp0"
rem Asks which channel profile, how many Shorts, then who writes them (Claude, Gemini, or both to compare).
".venv\Scripts\python.exe" make_shorts.py
pause
