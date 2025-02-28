@echo off
title Einfacher Abhaengigkeiten-Installer

echo =======================================================
echo            Einfacher Abhaengigkeiten-Installer
echo =======================================================
echo.

REM Versuche, mit Admin-Rechten zu starten
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo HINWEIS: Dieses Skript hat keine Administratorrechte.
    echo Einige Installationen koennten fehlschlagen.
    echo.
    echo Druecken Sie eine beliebige Taste, um fortzufahren...
    pause >nul
) else (
    echo Administrator-Rechte: OK
)

echo.
echo Python-Version wird ueberprueft...
python --version
if %errorlevel% neq 0 (
    echo Python wurde nicht gefunden!
    echo Bitte installieren Sie Python und stellen Sie sicher, dass es im PATH ist.
    echo.
    echo Druecken Sie eine beliebige Taste zum Beenden...
    pause >nul
    exit /b 1
)

echo.
echo Starte das Installations-Hauptmenue...
echo.

REM Direkter Aufruf ohne Umwege
python simple_install.py

echo.
echo Druecken Sie eine beliebige Taste zum Beenden...
pause >nul