@echo off
echo ===================================================
echo  Bildprozessor Pro - Windows EXE Erstellungsskript
echo ===================================================
echo.

echo Pruefe, ob PyInstaller installiert ist...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller ist nicht installiert. Installiere jetzt...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo Fehler bei der Installation von PyInstaller.
        exit /b 1
    )
    echo PyInstaller wurde erfolgreich installiert.
) else (
    echo PyInstaller ist bereits installiert.
)

echo.
echo Prüfe, ob alle Abhängigkeiten installiert sind...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Warnung: Einige Abhängigkeiten konnten nicht installiert werden.
    echo Versuche trotzdem fortzufahren...
)

echo.
echo Erstelle einmalige Build-Version...
for /f "tokens=2 delims==" %%a in ('wmic os get localdatetime /value') do set datetime=%%a
set build_version=%datetime:~0,8%-%datetime:~8,6%

echo.
echo Erstelle Windows-Executable mit PyInstaller...
echo Build-Version: %build_version%

pyinstaller --onefile ^
    --name "BildprozessorPro_%build_version%" ^
    --icon=resources/icon.ico ^
    --add-data "resources;resources" ^
    --hidden-import tkinter ^
    --hidden-import PIL ^
    --hidden-import numpy ^
    --hidden-import pdf2image ^
    --hidden-import pytesseract ^
    --hidden-import paddleocr ^
    --hidden-import paddle ^
    main.py

if %errorlevel% neq 0 (
    echo Fehler beim Erstellen der EXE-Datei.
    exit /b 1
)

echo.
echo Kopiere zusätzliche Dateien...
mkdir dist\doc 2>nul
xcopy /E /I /Y doc dist\doc
copy README.md dist\
copy requirements.txt dist\

echo.
echo Erstelle ZIP-Archiv...
cd dist
powershell -command "Compress-Archive -Path .\* -DestinationPath ..\BildprozessorPro_%build_version%.zip -Force"
cd ..

echo.
echo Build erfolgreich abgeschlossen!
echo Die EXE-Datei befindet sich im 'dist'-Ordner.
echo Eine ZIP-Datei wurde ebenfalls erstellt: BildprozessorPro_%build_version%.zip
echo.
echo ===================================================