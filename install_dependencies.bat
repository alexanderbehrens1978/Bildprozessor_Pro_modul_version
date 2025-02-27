@echo off
chcp 1252 >nul
title Bildprozessor Pro - Abhängigkeiten installieren

echo =======================================================
echo               Bildprozessor Pro
echo         Installation der Abhängigkeiten
echo =======================================================
echo.

REM Versuche, mit Admin-Rechten zu starten
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo HINWEIS: Dieses Skript hat keine Administratorrechte.
    echo Einige Installationen könnten fehlschlagen.
    echo.
    echo Drücken Sie eine beliebige Taste, um fortzufahren...
    pause >nul
) else (
    echo Administrator-Rechte: OK
)

echo.
echo Python-Version wird überprüft...
python --version
if %errorlevel% neq 0 (
    echo Python wurde nicht gefunden!
    echo Bitte installieren Sie Python und stellen Sie sicher, dass es im PATH ist.
    echo.
    echo Drücken Sie eine beliebige Taste zum Beenden...
    pause >nul
    exit /b 1
)

echo.
echo Starte die Installation der Abhängigkeiten...
echo.

REM Führe das Python-Installationsskript aus
python install_dependencies.py

echo.
echo Wenn alle Abhängigkeiten erfolgreich installiert wurden,
echo können Sie nun die Anwendung starten:
echo.
echo    python main.py
echo.
echo Drücken Sie eine beliebige Taste zum Beenden...
pause >nul