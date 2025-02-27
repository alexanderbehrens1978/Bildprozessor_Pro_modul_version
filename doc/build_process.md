Bildprozessor Pro - Build-Prozess
Diese Dokumentation beschreibt den Build-Prozess für die Erstellung ausführbarer Dateien des Bildprozessor Pro.
Inhaltsverzeichnis

Voraussetzungen
Windows-Build
Linux/macOS-Build
Build-Parameter
Bekannte Probleme
Optimierung der ausführbaren Dateien

Voraussetzungen
Für den Build-Prozess benötigen Sie:

Python 3.6 oder höher
PyInstaller (wird automatisch installiert, falls nicht vorhanden)
Alle Abhängigkeiten aus requirements.txt
500 MB freien Festplattenspeicher
Internetverbindung (für die Installation fehlender Pakete)

Windows-Build
Der Build-Prozess unter Windows verwendet das Skript build_exe.bat.
Schritte zum Erstellen einer Windows-EXE:

Öffnen Sie eine Eingabeaufforderung im Projektverzeichnis
Führen Sie den Befehl aus:
Copybuild_exe.bat

Das Skript führt folgende Aktionen aus:

Überprüft, ob PyInstaller installiert ist, und installiert es bei Bedarf
Stellt sicher, dass alle Abhängigkeiten installiert sind
Erstellt eine zeitgestempelte Version der ausführbaren Datei
Kompiliert die Anwendung mit PyInstaller im "onefile"-Modus
Kopiert Dokumentation und erforderliche Dateien in den Ausgabeordner
Erstellt ein ZIP-Archiv der kompilierten Anwendung



Die ausführbare Datei wird im dist-Ordner erstellt und enthält alles, was für die Ausführung der Anwendung erforderlich ist.
Linux/macOS-Build
Der Build-Prozess unter Linux und macOS verwendet das Skript build_exe.sh.
Schritte zum Erstellen einer Linux/macOS-Executable:

Öffnen Sie ein Terminal im Projektverzeichnis
Machen Sie das Skript ausführbar:
Copychmod +x build_exe.sh

Führen Sie das Skript aus:
Copy./build_exe.sh

Das Skript führt ähnliche Aktionen wie das Windows-Skript aus

Build-Parameter
Die Build-Skripte verwenden folgende PyInstaller-Parameter:

--onefile: Erstellt eine einzelne ausführbare Datei
--name: Setzt den Namen der ausführbaren Datei (mit Zeitstempel)
--icon: (nur Windows) Setzt das Anwendungssymbol
--add-data: Fügt Ressourcendateien hinzu
--hidden-import: Fügt explizite Importe hinzu, die PyInstaller möglicherweise nicht automatisch erkennt

Anpassen der Build-Parameter:
Sie können die Skripte bearbeiten, um die Build-Parameter anzupassen, z.B.:

Entfernen des --onefile-Parameters und Hinzufügen von --onedir, um ein Verzeichnis statt einer einzelnen Datei zu erstellen
Hinzufügen von --noconsole (Windows) oder --windowed (Linux/macOS), um die Konsole auszublenden
Hinzufügen von --clean, um vor dem Build das Cache-Verzeichnis zu bereinigen

Bekannte Probleme
Große Dateigröße
Die erstellte ausführbare Datei kann relativ groß sein (100-150 MB), da sie alle Abhängigkeiten enthält, einschließlich:

Python-Interpreter
Tkinter
PIL und seine Abhängigkeiten
NumPy
OCR-Bibliotheken (PaddleOCR, Tesseract-Bindungen)

Lange Startzeit
Bei der ersten Ausführung kann die Anwendung eine längere Startzeit haben, besonders im --onefile-Modus, da die Dateien zuerst in ein temporäres Verzeichnis extrahiert werden müssen.
Fehlende Abhängigkeiten
Trotz des --hidden-import-Parameters kann PyInstaller manchmal Abhängigkeiten übersehen. Wenn die ausführbare Datei mit Fehlern zu fehlenden Modulen startet, fügen Sie diese Module zum --hidden-import-Parameter hinzu.
Antivirus-Warnungen
Einige Antivirenprogramme können bei ausführbaren Dateien, die mit PyInstaller erstellt wurden, Fehlalarme auslösen. Dies ist ein bekanntes Problem und kann häufig ignoriert werden.
Optimierung der ausführbaren Dateien
Reduzieren der Dateigröße
Um die Größe der ausführbaren Datei zu reduzieren:

Verwenden Sie UPX-Komprimierung (optional in PyInstaller):
Copy--upx-dir=/path/to/upx

Entfernen Sie unnötige Pakete:
Copy--exclude-module matplotlib

Verwenden Sie den --onedir-Modus statt --onefile:
Copy--onedir


Verbessern der Startzeit

Verwenden Sie den --onedir-Modus für schnelleren Start
Reduzieren Sie die Anzahl der versteckten Importe auf das Notwendige
Erstellen Sie den Build mit --noupx, um auf UPX-Komprimierung zu verzichten

Mehrere Plattformen unterstützen
Um Builds für verschiedene Plattformen zu erstellen:

Verwenden Sie virtuelle Maschinen oder Docker-Container für plattformspezifische Builds
Führen Sie die Build-Skripte auf jeder Zielplattform aus
Sammeln Sie die ausführbaren Dateien in einem zentralen Repository