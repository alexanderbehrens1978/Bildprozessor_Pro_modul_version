Bildprozessor Pro - Architektur
Übersicht
Die Anwendung ist nach einem modularen Prinzip aufgebaut, um eine klare Trennung von Verantwortlichkeiten zu gewährleisten und die Wartbarkeit zu verbessern. Die Architektur folgt grob dem MVC-Muster (Model-View-Controller), wobei:

Models: Datenstrukturen und Geschäftslogik (Filterverarbeitung, Einstellungen, OCR-Engine)
Views: Benutzeroberfläche (UI-Komponenten, Dialoge)
Controller: Verbindungsschicht zwischen Modellen und Views (hauptsächlich in der Hauptanwendungsklasse)

Verzeichnisstruktur
Copybildprozessor_pro/
│
├── main.py                     # Haupteinstiegspunkt der Anwendung
│
├── utils/                      # Hilfsmodule und Dienstprogramme
│   ├── path_utils.py           # Funktionen für Pfadoperationen
│   ├── package_installer.py    # Automatische Installation von Abhängigkeiten
│   └── poppler_utils.py        # Poppler-spezifische Funktionen
│
├── models/                     # Datenmodelle und Geschäftslogik
│   └── settings.py             # Verwaltung von Anwendungseinstellungen
│
├── ui/                         # Benutzeroberflächen-Module
│   ├── main_window.py          # Hauptanwendungsfenster
│   ├── menu.py                 # Menüerstellung
│   ├── image_canvas.py         # Bildanzeige-Canvas
│   ├── filter_layers.py        # UI für Filterebenen
│   └── ocr_ui.py               # OCR-Dialogfenster
│
├── image_processing/           # Bildverarbeitungslogik
│   └── filters.py              # Implementierung von Bildfiltern
│
├── ocr/                        # OCR-Funktionalität
│   ├── ocr_engine.py           # OCR-Engine-Abstraktion
│   └── ocr_installer.py        # Automatische Installation von OCR-Engines
│
└── doc/                        # Dokumentation
    ├── architecture.md         # Dieses Dokument
    ├── modules.md              # Modulbeschreibungen
    ├── developer_guide.md      # Entwicklerhandbuch
    ├── user_guide.md           # Benutzerhandbuch
    ├── installation.md         # Installationsanleitung
    └── ocr_integration.md      # OCR-spezifische Dokumentation
Datenfluss

Bild laden:

Benutzer wählt ein Bild oder PDF
main_window.py ruft PDF-Konvertierung auf (falls nötig)
Originalansicht wird im linken Canvas angezeigt


Filteranwendung:

Benutzer aktiviert/konfiguriert Filter in der UI
filter_layers.py meldet Änderungen
main_window.py ruft filters.py auf, um Filter anzuwenden
Verarbeitetes Bild wird im rechten Canvas angezeigt


OCR-Verarbeitung:

Benutzer startet OCR über Menü
ocr_ui.py zeigt OCR-Dialog
ocr_engine.py verarbeitet das Bild
Erkannter Text wird angezeigt und kann gespeichert werden



Abhängigkeiten zwischen Modulen
Die folgende Grafik zeigt die Hauptabhängigkeiten zwischen den Modulen:
Copymain.py ────────────┐
        │           │
        ▼           ▼
  utils/ ◄─── models/ ◄─────┐
                │           │
                ▼           │
              ui/ ◄─────────┤
                │           │
                ▼           │
     image_processing/ ◄────┤
                            │
                            │
              ocr/ ◄────────┘

main.py initialisiert die Anwendung und die Haupt-UI
utils/ liefert Hilfsfunktionen für alle anderen Module
models/ verwaltet die Daten und Einstellungen
ui/ enthält alle Benutzeroberflächen-Komponenten, abhängig von den Modellen
image_processing/ implementiert die Bildverarbeitungslogik
ocr/ fügt OCR-Funktionalität hinzu, unabhängig vom Rest der Anwendung

Erweiterbarkeit
Die modulare Struktur ermöglicht einfache Erweiterungen:

Neue Filter: Fügen Sie Filter in filters.py hinzu und aktualisieren Sie die Filterliste in filter_layers.py
Neue UI-Komponenten: Erstellen Sie neue Dialoge oder Widgets in ui/
Neue OCR-Engines: Erweitern Sie ocr_engine.py mit neuen OCR-Implementierungen

Ressourcenmanagement

PIL-Bilder werden explizit kopiert, um Änderungen am Original zu vermeiden
Temporäre Dateien werden nach Gebrauch bereinigt
Threading wird für langlaufende Operationen (OCR, Installationen) verwendet, um die UI reaktionsfähig zu halten