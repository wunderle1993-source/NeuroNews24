@echo off
echo ===================================================
echo             NEURONEWS24 - BOT-STARTER
echo ===================================================
echo.
echo Dieses Programm startet deinen Telegram-Bot.
echo Es prueft, ob alles bereit ist, und installiert 
echo fehlende Zusatzprogramme vollautomatisch.
echo.
echo ---------------------------------------------------
echo Schritt 1: Pruefe ob Python installiert ist...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [FEHLER] Python ist auf diesem PC nicht installiert!
    echo Bitte lade dir Python herunter und installiere es:
    echo https://www.python.org/ftp/python/3.11.2/python-3.11.2-amd64.exe
    echo.
    echo WICHTIG: Setze bei der Installation unbedingt den Haken bei:
    echo "[x] Add python.exe to PATH"
    echo.
    pause
    exit
)
echo [OK] Python wurde gefunden!
echo.
echo ---------------------------------------------------
echo Schritt 2: Installiere Zusatzprogramme (requirements)...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo [INFO] Zusatzprogramme konnten nicht automatisch installiert werden.
    echo Falls alles bereits installiert ist, versuchen wir trotzdem zu starten...
) else (
    echo [OK] Alle Zusatzprogramme sind erfolgreich installiert!
)
echo.
echo ---------------------------------------------------
echo Schritt 3: Starte den NeuroNews24 Bot...
echo.
python main.py
echo.
echo ---------------------------------------------------
echo Bot-Ausfuehrung beendet.
echo.
pause
