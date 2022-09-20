@echo off
NET SESSION >nul 2>&1
IF %ERRORLEVEL% EQU 0 (
    cls
    echo ONLY RUN ONCE
    pip install -U pyinstaller
    pip install -U requests
) ELSE (
    ECHO Run as Admin!
    PAUSE
)