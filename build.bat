@echo off
pyinstaller --icon icon.ico --onefile --noconsole Hunter.py
PAUSE
cls
echo Build is in /dist
PAUSE