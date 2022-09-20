@echo off
pyinstaller --onefile --noconsole Hunter.py
cls
echo Build is in /dist
PAUSE