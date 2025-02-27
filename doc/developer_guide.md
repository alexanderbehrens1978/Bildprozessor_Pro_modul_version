Bildprozessor Pro - Entwicklerhandbuch
Dieses Handbuch richtet sich an Entwickler, die den Bildprozessor Pro verstehen, erweitern oder anpassen möchten.
Entwicklungsumgebung einrichten
Voraussetzungen

Python 3.6 oder höher
Git (für Versionskontrolle)
Code-Editor oder IDE (empfohlen: Visual Studio Code, PyCharm)

Repository klonen
bashCopygit clone https://github.com/alexanderbehrens1978/Bildprozessor_Pro_modul_version.git
cd Bildprozessor_Pro_modul_version
Virtuelle Umgebung einrichten
bashCopy# Erstellen einer virtuellen Umgebung
python -m venv venv

# Aktivieren (Windows)
venv\Scripts\activate

# Aktivieren (Linux/macOS)
source venv/bin/activate

# Installieren der Abhängigkeiten
pip install -r requirements.txt
Projektstruktur verstehen
Die Anwendung ist modular aufgebaut, um eine klare Trennung der Verantwortlichkeiten zu gewährleisten. Siehe architecture.md für einen Überblick über die Architektur und modules.md für detaillierte Modulbeschreibungen.
Coding-Standards
Namenskonventionen

Modulnamen: Kleinbuchstaben mit Unterstrichen (snake_case), z.B. image_canvas.py
Klassennamen: CamelCase, z.B. ImageProcessorApp
Funktions- und Methodennamen: snake_case, z.B. load_image()
Konstanten: GROSSBUCHSTABEN_MIT_UNTERSTRICHEN, z.B. ENGINE_TESSERACT

Dokumentation

Jede Klasse und öffentliche Funktion sollte mit Docstrings dokumentiert sein
Komplexe Code-Abschnitte sollten mit Inline-Kommentaren erklärt werden
Verwenden Sie sprechende Variablennamen

Fehlerbehandlung

Verwenden Sie Try-Except-Blöcke, um Fehler abzufangen
Zeigen Sie dem Benutzer aussagekräftige Fehlermeldungen an
Protokollieren Sie Fehler für die Fehlerbehebung

Erweiterung des Codes
Hinzufügen eines neuen Filters

Fügen Sie die Filter-Funktion in image_processing/filters.py hinzu:

pythonCopyelif filter_name == "Mein_Neuer_Filter":
    # Filter-Implementierung
    # ...
    return modified_image

Aktualisieren Sie die Liste der Filter in ui/filter_layers.py:

pythonCopydef create_filter_options():
    return [
        # Bestehende Filter...
        "Mein_Neuer_Filter",
    ]
Hinzufügen einer neuen OCR-Engine

Erweitern Sie die Engine-Konstanten in ocr/ocr_engine.py:

pythonCopyENGINE_MEINE_NEUE_ENGINE = "meine_neue_engine"

Fügen Sie Funktionen zum Prüfen und Initialisieren der Engine hinzu:

pythonCopydef _check_meine_neue_engine(self):
    """Überprüft, ob Meine Neue Engine installiert ist"""
    try:
        # Überprüfungscode
        return True
    except:
        return False
        
def _init_meine_neue_engine(self):
    """Initialisiert Meine Neue Engine"""
    # Initialisierungscode

Erweitern Sie die Verarbeitungsmethode:

pythonCopydef _process_image_sync(self, image):
    # ...
    elif self.current_engine == self.ENGINE_MEINE_NEUE_ENGINE:
        return self._process_with_meine_neue_engine(image)
    # ...
    
def _process_with_meine_neue_engine(self, image):
    """Verarbeitet ein Bild mit Meiner Neuen Engine"""
    # Implementierung

Fügen Sie die Installationsfunktion in ocr/ocr_installer.py hinzu:

pythonCopydef install_meine_neue_engine(self):
    """Installiert Meine Neue Engine"""
    # Installationscode

Aktualisieren Sie die UI in ui/ocr_ui.py, um die neue Engine anzuzeigen.

Erstellen eines neuen UI-Dialogs

Erstellen Sie eine neue Datei in ui/, z.B. ui/mein_dialog.py:

pythonCopyimport tkinter as tk
from tkinter import ttk

class MeinDialog:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Mein Dialog")
        
        # UI-Komponenten erstellen
        
    def run(self):
        """Zeigt den Dialog modal an"""
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        self.parent.wait_window(self.dialog)

Integrieren Sie den Dialog in ui/main_window.py:

pythonCopyfrom ui.mein_dialog import MeinDialog

# ...

def show_mein_dialog(self):
    dialog = MeinDialog(self.root)
    dialog.run()

Fügen Sie einen Menüeintrag in ui/menu.py hinzu:

pythonCopymein_menu.add_command(label="Mein Dialog", command=app.show_mein_dialog)
Test-Strategie
Manuelle Tests

Testen Sie neue Funktionen mit verschiedenen Eingabebildern
Überprüfen Sie die Benutzeroberfläche auf Benutzerfreundlichkeit
Testen Sie die Anwendung auf verschiedenen Betriebssystemen

Automatische Tests (future)

Unit-Tests für Kernfunktionen
Integration-Tests für Modulzusammenarbeit
Automatisierte UI-Tests für Benutzeraktionen

Build-Prozess
Executable erstellen
bashCopy# Installieren von PyInstaller
pip install pyinstaller

# Erstellen einer ausführbaren Datei
pyinstaller --onefile --windowed main.py --name BildprozessorPro

# Mit zusätzlichen Abhängigkeiten (z.B. Poppler)
pyinstaller --onefile --windowed --add-data "poppler_bin;poppler_bin" main.py --name BildprozessorPro
Release-Prozess

Versionsnummer in ui/main_window.py aktualisieren
CHANGELOG.md aktualisieren
Executable erstellen und testen
Release-Tag in Git erstellen
Distributionspakete hochladen

Debugging-Tipps
Häufige Probleme

Importfehler: Überprüfen Sie die Modulpfade und Abhängigkeiten
UI-Probleme: Verwenden Sie print-Anweisungen oder Logging, um den Status zu überprüfen
Bildverarbeitungsfehler: Speichern Sie Zwischenergebnisse als Bilder zur Überprüfung

Debugging-Tools

Print-Debugging: Fügen Sie temporäre print-Anweisungen ein
Logging: Verwenden Sie das logging-Modul für strukturiertes Logging
Debugger: Verwenden Sie den Debugger Ihrer IDE für Schritt-für-Schritt-Debugging

Performance-Optimierung
Bildverarbeitung

Verarbeiten Sie große Bilder in niedrigerer Auflösung für die Vorschau
Optimieren Sie Filter-Algorithmen für häufig verwendete Operationen

UI-Reaktionsfähigkeit

Verwenden Sie Threading für langlaufende Operationen
Implementieren Sie Fortschrittsanzeigen für zeitaufwändige Aufgaben

Ressourcen und Referenzen

Tkinter-Dokumentation
Pillow (PIL) Dokumentation
PyInstaller-Dokumentation
Tesseract OCR-Dokumentation
PaddleOCR-Dokumentation