Bildprozessor Pro - OCR-Integration
Diese Dokumentation beschreibt im Detail die OCR-Funktionalität (Optical Character Recognition) des Bildprozessor Pro, ihre Implementierung und Verwendung.
Inhaltsverzeichnis

Übersicht
Unterstützte OCR-Engines
Architektur der OCR-Integration
Installationsprozess
OCR-Verwendung
Sprachunterstützung
Erweiterte Funktionen
Fehlerbehebung
Entwicklungshinweise

Übersicht
Die OCR-Funktionalität ermöglicht es dem Bildprozessor Pro, Text aus Bildern zu erkennen und zu extrahieren. Dies ist besonders nützlich für:

Texterkennung in gescannten Dokumenten
Extrahieren von Text aus Fotos
Digitalisierung von gedruckten Materialien
Texterkennung in bearbeiteten Bildern

Unterstützte OCR-Engines
Der Bildprozessor Pro unterstützt zwei leistungsstarke OCR-Engines:
Tesseract OCR

Beschreibung: Open-Source-OCR-Engine, entwickelt von Google
Vorteile: Gute Texterkennung für klare Dokumente, breite Sprachunterstützung
Nachteile: Weniger genau bei komplexen Layouts oder niedrigerer Bildqualität
Betriebsmodi: Nur CPU-basiert
Empfohlen für: Klare Textdokumente mit einfachem Layout

PaddleOCR

Beschreibung: Moderne OCR-Engine auf Basis von Deep Learning (PaddlePaddle Framework)
Vorteile: Bessere Erkennung bei komplexen Layouts, robuster bei niedriger Bildqualität
Nachteile: Größerer Ressourcenbedarf, längere Initialisierungszeit
Betriebsmodi: CPU-Version und GPU-beschleunigte Version
Empfohlen für: Komplexe Layouts, mehrsprachige Dokumente, Bilder mit niedrigerer Qualität

Architektur der OCR-Integration
Die OCR-Funktionalität ist in mehrere Komponenten unterteilt:
1. OCR-Engine (ocr/ocr_engine.py)

Kernklasse: OCREngine
Verantwortlich für die Abstraktion verschiedener OCR-Implementierungen
Verarbeitet Bilder und extrahiert Text
Visualisiert erkannte Textbereiche

Hauptfunktionen:

process_image(): Verarbeitet ein Bild mit der ausgewählten Engine
set_engine(): Wechselt zwischen OCR-Engines
set_language(): Stellt die Erkennungssprache ein
draw_results_on_image(): Zeichnet Bounding Boxes um erkannten Text

2. OCR-Installer (ocr/ocr_installer.py)

Kernklasse: OCRInstaller
Verantwortlich für die automatische Installation von OCR-Engines
Plattformübergreifend (Windows, Linux, macOS)
Bietet visuelle Fortschrittsanzeige während der Installation

Hauptfunktionen:

install_tesseract(): Installiert Tesseract OCR
install_paddleocr(): Installiert PaddleOCR (CPU oder GPU)
check_tesseract(): Überprüft, ob Tesseract installiert ist
check_paddleocr(): Überprüft, ob PaddleOCR installiert ist

3. OCR-UI (ui/ocr_ui.py)

Kernklasse: OCRDialog
Bietet Benutzeroberfläche für OCR-Funktionen
Erlaubt die Auswahl von OCR-Engines und Sprachen
Zeigt Ergebnisse an und ermöglicht deren Verwendung

Hauptfunktionen:

on_scan_text(): Startet den OCR-Prozess
on_copy_text(): Kopiert erkannten Text in die Zwischenablage
on_save_text(): Speichert erkannten Text als Textdatei
on_show_boxes_change(): Schaltet die Anzeige von Textbereichen ein/aus

Installationsprozess
Tesseract OCR Installation
Windows

Herunterladen des Tesseract-Installers
Stille Installation mit vordefinierten Parametern
Setzen des Pfads in der Umgebungsvariable

Linux

Installation über den Paketmanager (apt, dnf, pacman)
Installation der Entwicklungsbibliotheken

macOS

Installation über Homebrew
Installation von Sprachpaketen

PaddleOCR Installation

Installation der Python-Abhängigkeiten (numpy, opencv-python, etc.)
Installation von PaddlePaddle (CPU oder GPU-Version)
Installation des PaddleOCR-Pakets
Herunterladen der Erkennungsmodelle

GPU-Unterstützung
Für die GPU-beschleunigte OCR (PaddleOCR):

Überprüfung der CUDA-Installation
Installation der GPU-Version von PaddlePaddle
Konfiguration für die GPU-Verwendung

OCR-Verwendung
Prozess der Texterkennung

Bildvorbereitung:

Laden eines Bildes
Optional: Anwenden von Filtern zur Verbesserung der Textsichtbarkeit
Konvertierung in ein Format, das von der OCR-Engine unterstützt wird


OCR-Verarbeitung:

Auswahl der OCR-Engine (Tesseract oder PaddleOCR)
Auswahl der Erkennungssprache
Starten des Erkennungsprozesses


Ergebnisverarbeitung:

Anzeige des erkannten Textes
Hervorhebung von Textbereichen im Bild
Möglichkeit zum Kopieren oder Speichern des Textes



Asynchrone Verarbeitung
Die OCR-Verarbeitung erfolgt asynchron, um die Benutzeroberfläche während der Texterkennung reaktionsfähig zu halten:

Verwendung von Threading für langlaufende Operationen
Fortschrittsanzeige während der Verarbeitung
Callback-Mechanismus für die Benachrichtigung über abgeschlossene Operationen

Sprachunterstützung
Tesseract OCR
Unterstützt über 100 Sprachen, darunter:

Deutsch (deu)
Englisch (eng)
Französisch (fra)
Italienisch (ita)
Spanisch (spa)
Russisch (rus)
Japanisch (jpn)
und viele mehr

PaddleOCR
Unterstützt mehrere Haupt-Sprachmodelle:

Deutsch (de)
Englisch (en)
Französisch (fr)
Italienisch (it)
Spanisch (es)
Russisch (ru)
Japanisch (japan)
Koreanisch (korean)
Chinesisch (ch)

Erweiterte Funktionen
Bounding Box Visualisierung

Markierung erkannter Textbereiche im Bild
Farbcodierung basierend auf Erkennungsgenauigkeit
Ein-/Ausschalten der Visualisierung

Verarbeitungsoptionen

Automatische Ausrichtungskorrektur (über PaddleOCR)
Erkennung von vertikalem Text (über PaddleOCR)
Mehrsprachige Erkennung

Integration mit Bildbearbeitung

Anwenden von Filtern zur Verbesserung der OCR-Genauigkeit
Vorgeschlagene Filterkombinationen für bessere OCR-Ergebnisse:

Kontrast erhöhen + Schärfen für undeutliche Texte
Binarisierung für Schwarz-Weiß-Dokumente
Kantenerkennung für Text auf komplexem Hintergrund



Fehlerbehebung
Häufige Probleme
Tesseract wurde nicht gefunden

Überprüfen Sie, ob Tesseract korrekt installiert ist
Stellen Sie sicher, dass Tesseract im System-PATH ist
Installieren Sie Tesseract über die Anwendung: OCR > Tesseract OCR installieren

PaddleOCR-Modelle werden nicht geladen

Überprüfen Sie die Internetverbindung
Stellen Sie sicher, dass genügend Festplattenspeicher verfügbar ist
Versuchen Sie eine Neuinstallation: OCR > PaddleOCR installieren

Schlechte Texterkennung

Versuchen Sie, die Bildqualität zu verbessern (Kontrast, Schärfe)
Wählen Sie die richtige Sprache für den Text
Probieren Sie eine andere OCR-Engine

GPU-Unterstützung funktioniert nicht

Überprüfen Sie, ob CUDA korrekt installiert ist
Stellen Sie sicher, dass eine kompatible NVIDIA-GPU vorhanden ist
Versuchen Sie die CPU-Version als Alternative

Diagnosetools

OCR-Engine-Status überprüfen: OCR > Tesseract/PaddleOCR installieren
Logs in der Konsole überprüfen (bei Start über Python)

Entwicklungshinweise
Erweiterung der OCR-Funktionalität
Hinzufügen einer neuen OCR-Engine

Fügen Sie eine neue Engine-Konstante in ocr_engine.py hinzu:
pythonCopyENGINE_NEW_ENGINE = "new_engine"

Implementieren Sie Methoden für die Initialisierung und Verarbeitung:
pythonCopydef _init_new_engine(self):
    # Initialisierungscode
    
def _process_with_new_engine(self, image):
    # Verarbeitungscode

Fügen Sie die Engine zur Erkennung hinzu:
pythonCopydef _detect_available_engines(self):
    # Bestehender Code
    try:
        # Code zum Überprüfen der neuen Engine
        available.append(self.ENGINE_NEW_ENGINE)
    except ImportError:
        pass

Erweitern Sie ocr_installer.py mit einer Installationsmethode:
pythonCopydef install_new_engine(self):
    # Installationscode

Aktualisieren Sie die UI in ocr_ui.py, um die neue Engine anzuzeigen.

Optimierung der Texterkennung

Vorverarbeitung von Bildern für bessere Ergebnisse
Nachbearbeitung des erkannten Textes
Implementierung von Wörterbuchkorrektur
Integration von Layout-Analyse für strukturierte Dokumente

Leistungsoptimierung

Zwischenspeichern von Modellen für schnellere Initialisierung
Optimierung der Bildgröße für den OCR-Prozess
Parallelisierung der Verarbeitung für Mehrfachbilder

Zukünftige Erweiterungen

Erkennung von handschriftlichem Text
OCR für Tabellen mit strukturierter Datenextraktion
Unterstützung für Formularerkennung
Batch-Verarbeitung mehrerer Bilder