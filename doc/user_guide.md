Bildprozessor Pro - Benutzerhandbuch
Inhaltsverzeichnis

Einführung
Installation
Erste Schritte
Bilder bearbeiten
Texterkennung (OCR)
Einstellungen verwalten
Tastenkombinationen
Fehlerbehebung

Einführung
Bildprozessor Pro ist eine leistungsstarke Anwendung zur Bildbearbeitung, die es Ihnen ermöglicht, verschiedene Filter und Effekte auf Ihre Bilder anzuwenden. Mit der integrierten OCR-Funktionalität (Optical Character Recognition) können Sie auch Text aus Bildern extrahieren.
Hauptfunktionen

Bearbeitung von Bildern mit 20 verschiedenen Filtern
Kombinieren mehrerer Filter mit anpassbarer Stärke
Sofortige Vorschau des Originalbilds und des bearbeiteten Bilds
PDF-Unterstützung mit automatischer Konvertierung
Texterkennung mit Tesseract OCR und PaddleOCR
GPU-beschleunigte OCR-Verarbeitung (optional)

Installation
Windows

Laden Sie die neueste Version der Anwendung von GitHub herunter
Entpacken Sie die Zip-Datei in einen Ordner Ihrer Wahl
Starten Sie die Anwendung durch Doppelklick auf BildprozessorPro.exe

Die Anwendung installiert fehlende Abhängigkeiten automatisch beim ersten Start.
Manuelle Installation aus dem Quellcode
Wenn Sie den Quellcode verwenden möchten:

Stellen Sie sicher, dass Python 3.6 oder höher installiert ist
Klonen Sie das Repository oder laden Sie den Quellcode herunter
Öffnen Sie eine Eingabeaufforderung im Projektverzeichnis
Führen Sie python main.py aus, um die Anwendung zu starten

Erste Schritte
Programmoberfläche
Nach dem Start der Anwendung sehen Sie folgende Hauptkomponenten:
Show Image (Screenshot nicht im Handbuch enthalten)

Menüleiste: Zugriff auf alle Funktionen
Linker Bildbereich: Zeigt das Originalbild
Rechter Bildbereich: Zeigt das bearbeitete Bild
Filterleiste: Konfiguration der Bildfilter
Statusleiste: Zeigt Informationen und aktuelle Aktionen

Ein Bild öffnen

Klicken Sie auf Datei > Bild laden in der Menüleiste
Wählen Sie ein Bild (JPG, PNG) oder eine PDF-Datei aus
Das Bild wird im linken Bereich angezeigt

PDF-Dateien
Wenn Sie eine PDF-Datei öffnen, wird automatisch die erste Seite als Bild konvertiert. Für diese Funktion wird Poppler benötigt, das bei Bedarf automatisch installiert wird.
Bilder bearbeiten
Filter anwenden
Sie können bis zu 5 Filter gleichzeitig auf Ihr Bild anwenden:

Aktivieren Sie einen Filter durch Anklicken der Checkbox neben "Filter 1", "Filter 2" usw.
Wählen Sie den gewünschten Filtertyp aus dem Dropdown-Menü
Passen Sie die Stärke des Filters mit dem Schieberegler an
Das bearbeitete Bild wird sofort im rechten Bereich angezeigt

Verfügbare Filter
FilterBeschreibungNegativInvertiert die Farben des BildesMultiplikationMultipliziert Pixelwerte mit einem FaktorHelligkeitErhöht oder verringert die HelligkeitKontrastVerstärkt oder reduziert den KontrastSchärfenMacht das Bild schärferWeichzeichnenMacht das Bild weicherGraustufenKonvertiert das Bild in GraustufenSepiaVerleiht dem Bild einen Sepia-FarbtonPosterizeReduziert die Anzahl der FarbenSolarizeErzeugt einen SolarisationseffektKantenerkennungHebt Kanten im Bild hervorEmbossErzeugt einen PrägeeffektEdge EnhanceVerbessert KantenDetailVerstärkt Details im BildSmoothGlättet das BildBinarizeKonvertiert in Schwarz/WeißGamma CorrectionKorrigiert die Gamma-WerteAdaptive ThresholdPasst Schwellenwerte automatisch anColor BoostVerstärkt die FarbsättigungCustomBenutzerdefinierter Filter
Beispiele für Filterkombinationen

Portrait verbessern:

Filter 1: Kontrast (0.3)
Filter 2: Schärfen (0.4)
Filter 3: Color Boost (0.2)


Künstlerischer Effekt:

Filter 1: Kantenerkennung (0.7)
Filter 2: Color Boost (0.5)
Filter 3: Solarize (0.3)



Bearbeitetes Bild speichern

Klicken Sie auf Datei > Bild speichern
Wählen Sie einen Speicherort und Dateinamen
Wählen Sie ein Dateiformat (PNG oder JPG)
Klicken Sie auf "Speichern"

Texterkennung (OCR)
Die OCR-Funktion ermöglicht es Ihnen, Text aus Ihren Bildern zu extrahieren.
OCR verwenden

Laden Sie ein Bild, das Text enthält
Wenden Sie bei Bedarf Filter an, um den Text besser lesbar zu machen
Klicken Sie auf OCR > Texterkennung (OCR)
Der OCR-Dialog wird geöffnet

OCR-Engine auswählen
Sie können zwischen verschiedenen OCR-Engines wählen:

Tesseract OCR: Zuverlässige Open-Source-OCR-Engine
PaddleOCR (CPU): Moderner OCR-Algorithmus (Standard-CPU-Version)
PaddleOCR (GPU): Schnellere Version, die GPU-Beschleunigung nutzt (benötigt kompatible NVIDIA-GPU)

Wenn eine Engine nicht installiert ist, können Sie sie direkt aus dem Dialog heraus installieren.
Sprache auswählen
Wählen Sie die Sprache des zu erkennenden Textes aus dem Dropdown-Menü. Die verfügbaren Sprachen hängen von der installierten OCR-Engine ab.
Text erkennen und verwenden

Klicken Sie auf "Text erkennen"
Der erkannte Text wird im rechten Bereich des Dialogs angezeigt
Textbereiche werden im Bild hervorgehoben
Sie können den Text in die Zwischenablage kopieren oder als Textdatei speichern

Einstellungen verwalten
Filtereinstellungen speichern
Wenn Sie eine Kombination von Filtern gefunden haben, die Ihnen gefällt, können Sie diese speichern:

Klicken Sie auf Datei > Einstellungen speichern
Die aktuellen Filtereinstellungen werden in der Datei settings.json gespeichert

Filtereinstellungen laden

Klicken Sie auf Datei > Einstellungen laden
Wählen Sie eine Einstellungsdatei aus
Die Filter werden entsprechend konfiguriert

Poppler-Einstellungen
Für die PDF-Unterstützung wird Poppler benötigt:

Automatische Installation: Klicken Sie auf Einstellungen > Poppler installieren
Manueller Pfad: Klicken Sie auf Einstellungen > Poppler Pfad setzen

Tastenkombinationen
TastenkombinationFunktionStrg+OBild öffnenStrg+SBild speichernStrg+QAnwendung beenden
Fehlerbehebung
Problem: Die Anwendung startet nicht

Stellen Sie sicher, dass Python 3.6 oder höher installiert ist
Überprüfen Sie, ob alle erforderlichen Abhängigkeiten installiert sind
Prüfen Sie die Berechtigungen des Verzeichnisses

Problem: PDF-Dateien können nicht geöffnet werden

Überprüfen Sie, ob Poppler korrekt installiert ist
Stellen Sie den Poppler-Pfad manuell ein

Problem: OCR funktioniert nicht

Überprüfen Sie, ob die OCR-Engine installiert ist
Installieren Sie die Engine über das OCR-Menü
Bei PaddleOCR mit GPU: Stellen Sie sicher, dass CUDA korrekt installiert ist

Problem: Filterfunktion hat keine Wirkung

Vergewissern Sie sich, dass die Checkbox des Filters aktiviert ist
Erhöhen Sie die Stärke des Filters mit dem Schieberegler
Testen Sie den Filter mit einem anderen Bild

Kontakt und Support
Bei weiteren Problemen oder Fragen wenden Sie sich bitte an:

E-Mail: info@alexanderbehrens.com
GitHub Issues: Bildprozessor Pro Issues