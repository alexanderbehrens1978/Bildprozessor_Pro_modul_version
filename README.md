Bildprozessor Pro
Über
Bildprozessor Pro ist eine Desktop-Anwendung zur Bildbearbeitung, die verschiedene Filter und Effekte auf Bilder anwenden kann. Die Anwendung unterstützt auch PDF-Dateien, die in bearbeitbare Bilder umgewandelt werden können. Ab Version 1.1 bietet die Anwendung auch OCR-Funktionalität zur Texterkennung.
Funktionen

Laden von Bildern und PDF-Dateien
Anwendung von bis zu 5 Filtern gleichzeitig mit einstellbarer Stärke
Vorschau von Original- und bearbeitetem Bild nebeneinander
Speichern von bearbeiteten Bildern
Speichern und Laden von Filtereinstellungen
Texterkennung (OCR) mit Tesseract und PaddleOCR
Unterstützung für GPU-beschleunigte OCR

Installation
Voraussetzungen
Die Anwendung installiert automatisch alle benötigten Python-Pakete beim ersten Start:

pillow (PIL)
pdf2image
numpy
matplotlib
pytesseract (für Tesseract OCR)
paddleocr (für PaddleOCR)

Poppler für PDF-Unterstützung
Für die PDF-Unterstützung wird Poppler benötigt. Die Anwendung kann Poppler automatisch installieren:

Starten Sie die Anwendung
Wählen Sie im Menü "Einstellungen" → "Poppler installieren"

Bei Problemen mit der automatischen Installation können Sie Poppler auch manuell installieren:
Windows

Laden Sie Poppler für Windows herunter: https://github.com/oschwartz10612/poppler-windows/releases/
Extrahieren Sie die ZIP-Datei
Wählen Sie im Menü "Einstellungen" → "Poppler Pfad setzen" und navigieren Sie zum "bin"-Ordner der extrahierten Dateien

Linux
Copysudo apt-get install poppler-utils
macOS
Copybrew install poppler
OCR-Engines
Die Anwendung unterstützt zwei OCR-Engines:
Tesseract OCR
Die Anwendung kann Tesseract automatisch installieren:

Wählen Sie im Menü "OCR" → "Tesseract OCR installieren"

Oder manuell installieren:
Windows

Laden Sie den Tesseract-Installer herunter: https://github.com/UB-Mannheim/tesseract/wiki
Führen Sie den Installer aus
Stellen Sie sicher, dass Tesseract zum PATH hinzugefügt wird

Linux
Copysudo apt-get install tesseract-ocr libtesseract-dev
macOS
Copybrew install tesseract
PaddleOCR
Die Anwendung kann PaddleOCR automatisch installieren:

Wählen Sie im Menü "OCR" → "PaddleOCR (CPU) installieren" oder "PaddleOCR (GPU) installieren"

Die GPU-Version erfordert eine NVIDIA-Grafikkarte mit CUDA-Unterstützung.
Verwendung
Bild laden

Klicken Sie auf "Datei" → "Bild laden"
Wählen Sie ein Bild oder eine PDF-Datei aus
Das Originalbild wird links angezeigt

Filter anwenden

Aktivieren Sie bis zu 5 Filter mit den Checkboxen
Wählen Sie den Filtertyp aus den Dropdown-Menüs
Stellen Sie die Stärke der Filter mit den Schiebereglern ein
Das bearbeitete Bild wird rechts angezeigt

Texterkennung (OCR)

Laden Sie ein Bild und wenden Sie gewünschte Filter an
Klicken Sie auf "OCR" → "Texterkennung (OCR)"
Wählen Sie die OCR-Engine und Sprache
Klicken Sie auf "Text erkennen"
Der erkannte Text wird angezeigt und kann kopiert oder gespeichert werden

Bild speichern

Klicken Sie auf "Datei" → "Bild speichern"
Wählen Sie einen Speicherort und ein Format
Das bearbeitete Bild wird gespeichert

Einstellungen speichern/laden

Klicken Sie auf "Datei" → "Einstellungen speichern", um Ihre aktuellen Filtereinstellungen zu speichern
Klicken Sie auf "Datei" → "Einstellungen laden", um gespeicherte Filtereinstellungen zu laden

Fehlerbehebung
PDF-Unterstützung funktioniert nicht

Überprüfen Sie, ob Poppler korrekt installiert ist
Stellen Sie sicher, dass der Poppler-Pfad korrekt gesetzt ist unter "Einstellungen" → "Poppler Pfad setzen"

OCR funktioniert nicht

Überprüfen Sie, ob die gewählte OCR-Engine installiert ist
Versuchen Sie, die OCR-Engine über das Menü "OCR" neu zu installieren
Bei PaddleOCR mit GPU: Stellen Sie sicher, dass CUDA korrekt installiert ist

Probleme beim Installieren von Paketen
Wenn die automatische Installation von Paketen fehlschlägt, können Sie sie manuell installieren:
Copy
pip install pillow pdf2image numpy matplotlib pytesseract paddleocr
Poppler kann nicht installiert werden
Bei Problemen mit der automatischen Poppler-Installation:

Versuchen Sie eine manuelle Installation wie oben beschrieben
Stellen Sie sicher, dass Sie über Administratorrechte verfügen
Überprüfen Sie Ihre Internetverbindung

Unterstützte Formate

Bilder: PNG, JPG, JPEG
Dokumente: PDF (erste Seite wird als Bild geladen)

Filtertypen
Die Anwendung bietet 20 verschiedene Filter, darunter:

Negativ
Multiplikation
Helligkeit/Kontrast
Schärfen/Weichzeichnen
Graustufen/Sepia
Kantenerkennung
und viele mehr

Systemanforderungen

Windows, Linux oder macOS
Python 3.6 oder höher
4 GB RAM empfohlen für größere Bilder
Für PaddleOCR mit GPU: NVIDIA-Grafikkarte mit CUDA-Unterstützung