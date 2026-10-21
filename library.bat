@echo off
cd /d "%~dp0"
rem Watch the looks, overlays and scene changes the AI invented for your Shorts; add the good ones to the library.
".venv\Scripts\python.exe" make_shorts.py library
pause
