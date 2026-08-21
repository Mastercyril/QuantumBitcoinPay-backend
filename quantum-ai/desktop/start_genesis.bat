@echo off
echo [Q.GENESIS] Auto-restart check...
tasklist /FI "WINDOWTITLE eq Q.GENESIS" 2>NUL | find /I "python.exe" >NUL
if "%ERRORLEVEL%"=="0" (
    echo [Q.GENESIS] Already running - skipping
) else (
    echo [Q.GENESIS] Starting Q.GENESIS...
    cd /d "C:\Users\josep\QuantumAI\Q_GENESIS"
    start "Q.GENESIS" python main.py
)
