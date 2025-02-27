# Bildprozessor Pro

## Überblick

Bildprozessor Pro ist eine leistungsstarke Desktop-Anwendung zur professionellen Bildbearbeitung mit zusätzlichen Funktionen wie PDF-Konvertierung und Texterkennung (OCR).

## Funktionen

- 🖼️ Laden von Bildern und PDF-Dateien
- 🎨 Anwendung von bis zu 5 Filtern gleichzeitig
  - Individuelle Filtereinstellungen
  - Vorschau von Original- und bearbeitetem Bild
- 💾 Speichern und Laden von Filtereinstellungen
- 📝 Texterkennung (OCR) mit:
  - Tesseract OCR
  - PaddleOCR
- 🚀 GPU-beschleunigte OCR-Unterstützung

## Systemanforderungen

- Betriebssystem: Windows, Linux oder macOS
- Python 3.6 oder höher
- Empfohlen: 4 GB RAM
- Für GPU-OCR: NVIDIA-Grafikkarte mit CUDA-Unterstützung

## Installation

### Automatische Paketinstallation

Die Anwendung installiert automatisch beim ersten Start:
- pillow (PIL)
- pdf2image
- numpy
- matplotlib
- pytesseract
- paddleocr

### Manuelle Paketinstallation

```bash
pip install pillow pdf2image numpy matplotlib pytesseract paddleocr
```

## Zusätzliche Abhängigkeiten

### Poppler (PDF-Unterstützung)

#### Windows
1. Download: [Poppler für Windows](https://github.com/oschwartz10612/poppler-windows/releases/)
2. ZIP-Datei extrahieren
3. Pfad in den Einstellungen setzen

#### Linux
```bash
sudo apt-get install poppler-utils
```

#### macOS
```bash
brew install poppler
```

### OCR-Engines

#### Tesseract OCR

##### Windows
1. [Tesseract-Installer herunterladen](https://github.com/UB-Mannheim/tesseract/wiki)
2. Installer ausführen
3. Zum PATH hinzufügen

##### Linux
```bash
sudo apt-get install tesseract-ocr libtesseract-dev
```

##### macOS
```bash
brew install tesseract
```

#### PaddleOCR

- CPU-Version: Im Menü "OCR" → "PaddleOCR (CPU) installieren"
- GPU-Version: Erfordert NVIDIA-Grafikkarte mit CUDA-Unterstützung

## Verwendung

### Bild laden
1. "Datei" → "Bild laden"
2. Bild oder PDF auswählen
3. Originalbild links anzeigen

### Filter anwenden
1. Bis zu 5 Filter aktivieren
2. Filtertyp auswählen
3. Filterstärke mit Schiebereglern einstellen
4. Bearbeitetes Bild rechts anzeigen

### Texterkennung (OCR)
1. Bild laden und ggf. filtern
2. "OCR" → "Texterkennung (OCR)"
3. OCR-Engine und Sprache wählen
4. "Text erkennen"
5. Text kopieren oder speichern

### Bild speichern
1. "Datei" → "Bild speichern"
2. Speicherort und Format wählen

## Unterstützte Formate

### Bilder
- PNG
- JPG
- JPEG

### Dokumente
- PDF (erste Seite wird als Bild geladen)

## Filtertypen

Über 20 verschiedene Filter, darunter:
- Negativ
- Multiplikation
- Helligkeit/Kontrast
- Schärfen/Weichzeichnen
- Graustufen/Sepia
- Kantenerkennung
- Und viele mehr

## Fehlerbehebung

### PDF-Unterstützung
- Poppler-Installation überprüfen
- Poppler-Pfad korrekt setzen

### OCR-Probleme
- OCR-Engine-Installation überprüfen
- Neuinstallation über Menü
- Bei GPU-PaddleOCR: CUDA-Installation überprüfen

## Lizenz

[Bitte Lizenzinformationen hier einfügen]

## Mitwirkende

[Bitte Mitwirkende hier auflisten]

## Kontakt

[Kontaktinformationen hier einfügen]
