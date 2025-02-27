#!/bin/bash

echo "==================================================="
echo " Bildprozessor Pro - Linux/macOS Build-Skript"
echo "==================================================="
echo

# Überprüfe, ob PyInstaller installiert ist
echo "Prüfe, ob PyInstaller installiert ist..."
if ! pip show pyinstaller &> /dev/null; then
    echo "PyInstaller ist nicht installiert. Installiere jetzt..."
    pip install pyinstaller
    if [ $? -ne 0 ]; then
        echo "Fehler bei der Installation von PyInstaller."
        exit 1
    fi
    echo "PyInstaller wurde erfolgreich installiert."
else
    echo "PyInstaller ist bereits installiert."
fi

echo
echo "Prüfe, ob alle Abhängigkeiten installiert sind..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Warnung: Einige Abhängigkeiten konnten nicht installiert werden."
    echo "Versuche trotzdem fortzufahren..."
fi

echo
echo "Erstelle einmalige Build-Version..."
build_version=$(date +"%Y%m%d-%H%M%S")

echo
echo "Erstelle ausführbare Datei mit PyInstaller..."
echo "Build-Version: $build_version"

pyinstaller --onefile \
    --name "BildprozessorPro_$build_version" \
    --add-data "resources:resources" \
    --hidden-import tkinter \
    --hidden-import PIL \
    --hidden-import numpy \
    --hidden-import pdf2image \
    --hidden-import pytesseract \
    --hidden-import paddleocr \
    --hidden-import paddle \
    main.py

if [ $? -ne 0 ]; then
    echo "Fehler beim Erstellen der ausführbaren Datei."
    exit 1
fi

echo
echo "Kopiere zusätzliche Dateien..."
mkdir -p dist/doc
cp -r doc/* dist/doc/
cp README.md dist/
cp requirements.txt dist/

echo
echo "Erstelle ZIP-Archiv..."
cd dist
zip -r "../BildprozessorPro_$build_version.zip" ./*
cd ..

echo
echo "Build erfolgreich abgeschlossen!"
echo "Die ausführbare Datei befindet sich im 'dist'-Ordner."
echo "Eine ZIP-Datei wurde ebenfalls erstellt: BildprozessorPro_$build_version.zip"
echo
echo "==================================================="

# Mache das Skript ausführbar
chmod +x dist/BildprozessorPro_$build_version