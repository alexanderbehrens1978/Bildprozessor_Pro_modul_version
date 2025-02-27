Bildprozessor Pro - Modulbeschreibungen
Diese Dokumentation beschreibt die einzelnen Module der Anwendung, ihre Funktionen und Verantwortlichkeiten.
Hauptmodul
main.py

Zweck: Einstiegspunkt der Anwendung
Funktionen:

Initialisiert das Tkinter-Hauptfenster
Überprüft und installiert benötigte Python-Pakete
Startet die Hauptanwendung


Abhängigkeiten:

utils/package_installer.py
ui/main_window.py



Dienstprogramme (utils/)
path_utils.py

Zweck: Stellt Hilfsfunktionen für Pfadoperationen bereit
Funktionen:

get_program_path(): Ermittelt den Pfad, in dem das Programm ausgeführt wird


Verwendung: Wird für das Finden von Einstellungsdateien und Installationspfaden verwendet

package_installer.py

Zweck: Automatische Installation von Python-Paketen
Funktionen:

check_and_install_packages(): Überprüft, ob benötigte Pakete installiert sind, und installiert fehlende
Unterstützende Funktionen für die Installation mit Fortschrittsanzeige


Verwendung: Wird beim Programmstart aufgerufen, um sicherzustellen, dass alle Abhängigkeiten verfügbar sind

poppler_utils.py

Zweck: Funktionen für Poppler (PDF-Unterstützung)
Funktionen:

install_poppler(): Installiert Poppler automatisch
set_poppler_path(): Setzt den Pfad zu einer bestehenden Poppler-Installation
get_poppler_path(): Ermittelt den aktuellen Poppler-Pfad


Verwendung: Wird für die PDF-zu-Bild-Konvertierung verwendet

Modelle (models/)
settings.py

Zweck: Verwaltung von Anwendungseinstellungen
Klassen:

SettingsManager: Lädt, speichert und verwaltet Anwendungseinstellungen


Funktionen:

load_default_settings(): Lädt Einstellungen aus settings.json
create_default_settings_file(): Erstellt eine Standard-Einstellungsdatei
save_settings(): Speichert Einstellungen in einer Datei
load_settings(): Lädt Einstellungen aus einer benutzerdefinierten Datei


Verwendung: Verwaltet Filter-Einstellungen und Anwendungskonfiguration

Benutzeroberfläche (ui/)
main_window.py

Zweck: Hauptfenster der Anwendung
Klassen:

ImageProcessorApp: Hauptanwendungsklasse


Funktionen:

Initialisierung des Hauptfensters
Bildlade- und -speicherfunktionen
Filter-Aktualisierung
OCR-Integration


Verwendung: Zentraler Controller für alle Anwendungsfunktionen

menu.py

Zweck: Erstellung des Anwendungsmenüs
Funktionen:

create_menu(): Erstellt das Hauptmenü der Anwendung


Verwendung: Wird von main_window.py verwendet, um das Menü zu erstellen

image_canvas.py

Zweck: Canvas für die Bildanzeige
Funktionen:

create_image_canvas(): Erstellt einen scrollbaren Canvas für Bilder
show_image(): Zeigt ein Bild im Canvas an


Verwendung: Für die Anzeige des Original- und des verarbeiteten Bildes

filter_layers.py

Zweck: UI für die Filterebenen
Funktionen:

create_filter_options(): Erstellt die Liste der verfügbaren Filter
create_layers_ui(): Erstellt die Benutzeroberfläche für die Filterebenen


Verwendung: Ermöglicht dem Benutzer, Filter zu aktivieren und zu konfigurieren

ocr_ui.py

Zweck: Benutzeroberfläche für OCR-Funktionen
Klassen:

OCRDialog: Dialog für die Texterkennung


Funktionen:

Anzeige von Bildern
OCR-Engine-Auswahl
Anzeige der OCR-Ergebnisse
Kopieren/Speichern von erkanntem Text


Verwendung: Wird für die Texterkennung in Bildern verwendet

Bildverarbeitung (image_processing/)
filters.py

Zweck: Implementierung von Bildfiltern
Funktionen:

apply_filter(): Wendet einen Filter auf ein Bild an
Implementierung von 20 verschiedenen Filtern


Verwendung: Wird für die Bildverarbeitung verwendet

OCR-Funktionalität (ocr/)
ocr_engine.py

Zweck: OCR-Engine-Abstraktion
Klassen:

OCREngine: Hauptklasse für OCR-Funktionen


Funktionen:

Initialisierung verschiedener OCR-Engines
Textextraktion aus Bildern
Visualisierung von erkanntem Text


Verwendung: Wird für die Texterkennung in Bildern verwendet

ocr_installer.py

Zweck: Automatische Installation von OCR-Engines
Klassen:

OCRInstaller: Installiert und konfiguriert OCR-Engines


Funktionen:

Installation von Tesseract OCR
Installation von PaddleOCR (mit/ohne GPU)
Überprüfung der verfügbaren OCR-Engines


Verwendung: Wird für die Installation und Konfiguration von OCR-Engines verwendet

Klassendiagramm (Hauptklassen)
Copy+-------------------+      +----------------+      +-------------+
| ImageProcessorApp |----->| SettingsManager|----->| OCRInstaller|
+-------------------+      +----------------+      +-------------+
        |                         |                      |
        v                         |                      v
+-------------------+             |             +-------------+
| UI Components     |             |             | OCREngine   |
| (Canvas, Filters) |             |             +-------------+
+-------------------+             |                    |
        |                         |                    |
        v                         v                    v
+---------------------------------------+      +-------------+
| Image Processing (apply_filter)       |----->| OCRDialog   |
+---------------------------------------+      +-------------+
Funktionsweise der Hauptkomponenten

Hauptanwendung (ImageProcessorApp):

Koordiniert alle Anwendungsfunktionen
Reagiert auf Benutzeraktionen
Verwaltet Bildänderungen


Einstellungen (SettingsManager):

Lädt und speichert Anwendungseinstellungen
Verwaltet Standardkonfigurationen


Bildverarbeitung (apply_filter):

Wendet Filter auf Bilder an
Verarbeitet Bildtransformationen


OCR-System (OCREngine):

Abstrahiert verschiedene OCR-Implementierungen
Erkennt Text in Bildern
Visualisiert erkannten Text


OCR-Installer (OCRInstaller):

Installiert OCR-Engines
Konfiguriert Systemabhängigkeiten


OCR-Dialog (OCRDialog):

Bietet Benutzeroberfläche für OCR-Funktionen
Zeigt Ergebnisse an
Ermöglicht Interaktion mit erkanntem Text