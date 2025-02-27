Bildprozessor Pro - Installationsanleitung
Diese Anleitung führt Sie durch die Installation des Bildprozessor Pro auf verschiedenen Betriebssystemen.
Inhaltsverzeichnis

Voraussetzungen
Windows-Installation
Linux-Installation
macOS-Installation
Installation aus dem Quellcode
Abhängigkeiten
Systemanforderungen
Problembehandlung

Voraussetzungen
Für die ausführbare Datei (Windows):

Windows 7 oder höher (64-Bit empfohlen)
Mindestens 4 GB RAM
500 MB freier Festplattenspeicher

Für die Installation aus dem Quellcode:

Python 3.6 oder höher
pip (Python-Paketmanager)
Git (für die Versionskontrolle, optional)

Windows-Installation
Option 1: Ausführbare Datei (Empfohlen)

Laden Sie die neueste Version des Bildprozessor Pro von der Releases-Seite herunter.
Entpacken Sie die ZIP-Datei in einen Ordner Ihrer Wahl.
Starten Sie die Anwendung durch Doppelklick auf BildprozessorPro.exe.

Bei der ersten Ausführung werden möglicherweise zusätzliche Abhängigkeiten installiert. Bitte folgen Sie den Anweisungen auf dem Bildschirm.
Option 2: Portable Version
Für eine portable Version ohne Installation:

Laden Sie die Datei BildprozessorPro_portable.zip herunter.
Entpacken Sie die ZIP-Datei in einen beliebigen Ordner (z.B. auf einem USB-Stick).
Starten Sie die Anwendung durch Doppelklick auf BildprozessorPro.exe.

Linux-Installation
Debian/Ubuntu und Derivate

Installieren Sie die benötigten Abhängigkeiten:
bashCopysudo apt-get update
sudo apt-get install python3 python3-pip python3-tk libpoppler-cpp-dev tesseract-ocr

Klonen Sie das Repository oder laden Sie den Quellcode herunter:
bashCopygit clone https://github.com/alexanderbehrens1978/Bildprozessor_Pro_modul_version.git
cd Bildprozessor_Pro_modul_version

Installieren Sie die Python-Abhängigkeiten:
bashCopypip3 install -r requirements.txt

Starten Sie die Anwendung:
bashCopypython3 main.py


Fedora/RHEL/CentOS

Installieren Sie die benötigten Abhängigkeiten:
bashCopysudo dnf install python3 python3-pip python3-tkinter poppler-cpp-devel tesseract tesseract-devel

Fahren Sie wie bei Debian/Ubuntu mit den Schritten 2-4 fort.

Arch Linux

Installieren Sie die benötigten Abhängigkeiten:
bashCopysudo pacman -S python python-pip tk poppler tesseract

Fahren Sie wie bei Debian/Ubuntu mit den Schritten 2-4 fort.

macOS-Installation

Installieren Sie Homebrew, falls noch nicht geschehen:
bashCopy/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

Installieren Sie Python und die benötigten Abhängigkeiten:
bashCopybrew install python poppler tesseract

Klonen Sie das Repository oder laden Sie den Quellcode herunter:
bashCopygit clone https://github.com/alexanderbehrens1978/Bildprozessor_Pro_modul_version.git
cd Bildprozessor_Pro_modul_version

Installieren Sie die Python-Abhängigkeiten:
bashCopypip3 install -r requirements.txt

Starten Sie die Anwendung:
bashCopypython3 main.py


Installation aus dem Quellcode
Diese Methode funktioniert auf allen unterstützten Plattformen:

Stellen Sie sicher, dass Python 3.6 oder höher installiert ist:
bashCopypython --version  # oder python3 --version auf einigen Systemen

Klonen Sie das Repository oder laden Sie den Quellcode herunter:
bashCopygit clone https://github.com/alexanderbehrens1978/Bildprozessor_Pro_modul_version.git
cd Bildprozessor_Pro_modul_version

(Optional) Erstellen Sie eine virtuelle Umgebung:
bashCopypython -m venv venv

# Aktivieren auf Windows
venv\Scripts\activate

# Aktivieren auf Linux/macOS
source venv/bin/activate

Installieren Sie die Python-Abhängigkeiten:
bashCopypip install -r requirements.txt

Starten Sie die Anwendung:
bashCopypython main.py


Abhängigkeiten
Der Bildprozessor Pro verwendet die folgenden Hauptabhängigkeiten:
Python-Pakete

Pillow (PIL): Bildverarbeitung
pdf2image: PDF-zu-Bild-Konvertierung
numpy: Mathematische Operationen
matplotlib: Visualisierung (optional)
pytesseract: Schnittstelle zu Tesseract OCR
paddleocr: PaddleOCR-Engine

Externe Abhängigkeiten

Poppler: Für PDF-Unterstützung
Tesseract OCR: Für OCR-Funktionalität
CUDA (optional): Für GPU-beschleunigte OCR mit PaddleOCR

Die Anwendung installiert fehlende Python-Pakete automatisch. Externe Abhängigkeiten können auch über die Anwendung installiert werden.
Systemanforderungen
Minimale Anforderungen

Betriebssystem: Windows 7+, Ubuntu 18.04+, macOS 10.14+
Prozessor: Dual-Core 2 GHz
RAM: 4 GB
Festplattenspeicher: 500 MB
Bildschirmauflösung: 1280x720

Empfohlene Anforderungen

Betriebssystem: Windows 10/11, Ubuntu 20.04+, macOS 12+
Prozessor: Quad-Core 3 GHz
RAM: 8 GB oder mehr
Festplattenspeicher: 1 GB
Bildschirmauflösung: 1920x1080
Für GPU-beschleunigte OCR: NVIDIA-GPU mit CUDA-Unterstützung

Problembehandlung
Fehlende Abhängigkeiten
Wenn Python-Pakete fehlen, versucht die Anwendung, diese automatisch zu installieren. Bei Problemen können Sie die Pakete manuell installieren:
bashCopypip install pillow pdf2image numpy pytesseract paddleocr
Poppler-Installation schlägt fehl
Windows

Laden Sie Poppler für Windows manuell herunter: https://github.com/oschwartz10612/poppler-windows/releases/
Extrahieren Sie die ZIP-Datei
Setzen Sie den Poppler-Pfad in der Anwendung: Einstellungen > Poppler Pfad setzen

Linux
Bei Problemen mit der automatischen Installation:
bashCopysudo apt-get install poppler-utils  # Debian/Ubuntu
sudo dnf install poppler-utils      # Fedora
sudo pacman -S poppler              # Arch Linux
macOS
Bei Problemen mit der automatischen Installation:
bashCopybrew install poppler
Tesseract OCR-Installation schlägt fehl
Windows

Laden Sie den Tesseract-Installer herunter: https://github.com/UB-Mannheim/tesseract/wiki
Führen Sie den Installer aus (Standardoptionen auswählen)
Starten Sie die Anwendung neu

Linux/macOS
Installieren Sie Tesseract über den Paketmanager:
bashCopy# Ubuntu/Debian
sudo apt-get install tesseract-ocr libtesseract-dev

# Fedora
sudo dnf install tesseract tesseract-devel

# Arch Linux
sudo pacman -S tesseract

# macOS
brew install tesseract
Weitere Hilfe
Wenn Sie weiterhin Probleme bei der Installation haben, besuchen Sie bitte die GitHub Issues-Seite oder kontaktieren Sie den Support unter info@alexanderbehrens.com.