# PowerShell-Skript zum Erstellen einer Windows-EXE mit PyInstaller

Write-Host "==================================================="
Write-Host " Bildprozessor Pro - Windows EXE Erstellungsskript"
Write-Host "==================================================="
Write-Host ""

# Prüfe, ob PyInstaller installiert ist
Write-Host "Prüfe, ob PyInstaller installiert ist..."
$pyinstallerInstalled = pip show pyinstaller 2>$null
if (-not $pyinstallerInstalled) {
    Write-Host "PyInstaller ist nicht installiert. Installiere jetzt..."
    pip install pyinstaller
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Fehler bei der Installation von PyInstaller." -ForegroundColor Red
        exit 1
    }
    Write-Host "PyInstaller wurde erfolgreich installiert." -ForegroundColor Green
} else {
    Write-Host "PyInstaller ist bereits installiert." -ForegroundColor Green
}

# Prüfe, ob alle Abhängigkeiten installiert sind
Write-Host ""
Write-Host "Prüfe, ob alle Abhängigkeiten installiert sind..."
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warnung: Einige Abhängigkeiten konnten nicht installiert werden." -ForegroundColor Yellow
    Write-Host "Versuche trotzdem fortzufahren..." -ForegroundColor Yellow
}

# Erstelle Ordner für die Ressourcen, falls sie nicht existieren
Write-Host ""
Write-Host "Erstelle Ressourcenordner, falls nicht vorhanden..."
if (-not (Test-Path -Path "resources")) {
    New-Item -Path "resources" -ItemType Directory | Out-Null
}

# Erstelle einmalige Build-Version
$buildVersion = Get-Date -Format "yyyyMMdd-HHmmss"
Write-Host ""
Write-Host "Erstelle Windows-Executable mit PyInstaller..."
Write-Host "Build-Version: $buildVersion" -ForegroundColor Cyan

# Führe PyInstaller aus
$pyinstallerCmd = "pyinstaller --onefile " +
                 "--name `"BildprozessorPro_$buildVersion`" " +
                 "--hidden-import tkinter " +
                 "--hidden-import PIL " +
                 "--hidden-import PIL._imagingtk " +
                 "--hidden-import PIL._tkinter_finder " +
                 "--hidden-import numpy " +
                 "--hidden-import pdf2image " +
                 "--hidden-import pytesseract " +
                 "--hidden-import paddleocr " +
                 "--hidden-import paddle " +
                 "main.py"

Write-Host "Ausführung des PyInstaller-Befehls: $pyinstallerCmd"
Invoke-Expression $pyinstallerCmd

if ($LASTEXITCODE -ne 0) {
    Write-Host "Fehler beim Erstellen der EXE-Datei." -ForegroundColor Red
    exit 1
}

# Kopiere zusätzliche Dateien
Write-Host ""
Write-Host "Kopiere zusätzliche Dateien..."
if (-not (Test-Path -Path "dist\doc")) {
    New-Item -Path "dist\doc" -ItemType Directory | Out-Null
}
Copy-Item -Path "doc\*" -Destination "dist\doc" -Recurse -Force
Copy-Item -Path "README.md" -Destination "dist\" -Force
Copy-Item -Path "requirements.txt" -Destination "dist\" -Force

# Erstelle ZIP-Archiv
Write-Host ""
Write-Host "Erstelle ZIP-Archiv..."
Compress-Archive -Path "dist\*" -DestinationPath "BildprozessorPro_$buildVersion.zip" -Force

Write-Host ""
Write-Host "Build erfolgreich abgeschlossen!" -ForegroundColor Green
Write-Host "Die EXE-Datei befindet sich im 'dist'-Ordner." -ForegroundColor Green
Write-Host "Eine ZIP-Datei wurde ebenfalls erstellt: BildprozessorPro_$buildVersion.zip" -ForegroundColor Green
Write-Host ""
Write-Host "==================================================="