"""Make ready-to-upload YouTube Shorts with no API keys.

Claude Code (headless) picks the niche and writes scripts + SEO, Wikimedia Commons
supplies images, Edge TTS does the voice, Pillow renders smooth motion + thumbnails,
ffmpeg mixes music/sound effects and encodes.

The code lives in the shortsmaker/ package; this file is what run.bat, fix.bat and library.bat run.
"""
from shortsmaker.cli import main

if __name__ == "__main__":
    main()
