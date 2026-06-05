@echo off
chcp 65001 >nul
echo ===================================================
echo             NEURONEWS24 - BOT-STARTER
echo ===================================================
echo.
echo Dieses Programm startet oder verwaltet deinen Bot lokal.
echo.
echo ---------------------------------------------------
echo Schritt 1: Prüfe ob Python installiert ist...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FEHLER] Python ist auf diesem PC nicht installiert!
    echo Bitte installiere Python und aktiviere "Add python.exe to PATH".
    pause
    exit /b 1
)
echo [OK] Python wurde gefunden!
echo.
echo ---------------------------------------------------
echo Schritt 2: Installiere Zusatzprogramme (requirements)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [WARNUNG] Zusatzprogramme konnten nicht komplett installiert werden.
    echo Wir machen trotzdem weiter.
) else (
    echo [OK] Alle Zusatzprogramme sind erfolgreich installiert!
)
echo.
echo ---------------------------------------------------
echo Was soll passieren?
echo.
echo   [1] JETZT EINMALIG POSTEN
echo   [2] TELEGRAM-DIAGNOSE PRÜFEN
echo   [3] WINDOWS-TASKS EINRICHTEN (08:30 und 17:00)
echo   [4] TASK ENTFERNEN
echo   [5] BEENDEN
echo.
set /p choice="Deine Wahl (1-5): "

if "%choice%"=="1" goto run_once
if "%choice%"=="2" goto test_telegram
if "%choice%"=="3" goto setup_task
if "%choice%"=="4" goto remove_task
goto end

:run_once
echo.
echo Starte NeuroNews24 jetzt einmal...
python main.py
echo.
pause
goto end

:test_telegram
echo.
echo Starte Telegram-Diagnose...
python test_telegram.py
echo.
pause
goto end

:setup_task
echo.
echo Richte lokale Standard-Times 08:30 und 17:00 ein...
schtasks /delete /tn "NeuroNews24_Daily" /f >nul 2>&1
schtasks /create /tn "NeuroNews24_0830" /tr "C:\Users\DAGOBERT\Desktop\run_neuronews24_daily.bat" /sc daily /st 08:30 /f
if %errorlevel% equ 0 (echo [OK] Task NeuroNews24_0830 wurde erstellt.) else (echo [FEHLER] Task NeuroNews24_0830 konnte nicht erstellt werden.)
schtasks /create /tn "NeuroNews24_1700" /tr "C:\Users\DAGOBERT\Desktop\run_neuronews24_daily.bat" /sc daily /st 17:00 /f
if %errorlevel% equ 0 (echo [OK] Task NeuroNews24_1700 wurde erstellt.) else (echo [FEHLER] Task NeuroNews24_1700 konnte nicht erstellt werden.)
echo.
pause
goto end

:remove_task
echo.
echo Entferne lokale Standard-Tasks...
schtasks /delete /tn "NeuroNews24_Daily" /f >nul 2>&1
schtasks /delete /tn "NeuroNews24_0830" /f >nul 2>&1
schtasks /delete /tn "NeuroNews24_1700" /f >nul 2>&1
echo [OK] NeuroNews24-Tasks wurden entfernt, falls vorhanden.
echo.
pause
goto end

:end
