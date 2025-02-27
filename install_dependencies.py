"""
Einfaches Skript zur Installation aller erforderlichen Abhängigkeiten
mit ausführlicher Ausgabe für Fehlerdiagnose
"""

import sys
import subprocess
import os
import time
from datetime import datetime
import threading

# Globale Variable für Abbruch
CANCEL_INSTALLATION = False


def get_timestamp():
	"""Gibt einen formattierten Zeitstempel zurück"""
	return datetime.now().strftime("%H:%M:%S")


def print_progress_bar(percent, prefix='', suffix='', length=40, fill='█'):
	"""
	Zeigt einen Fortschrittsbalken in der Konsole an
	"""
	if percent > 100:
		percent = 100
	percent_str = "{0:.1f}".format(percent)
	filled_length = int(length * percent / 100)
	bar = fill * filled_length + '-' * (length - filled_length)
	print(f'\r{prefix} |{bar}| {percent_str}% {suffix}', end='\r')
	if percent >= 100:
		print()


def install_package(package, verbose=False):
	"""
	Installiert ein einzelnes Paket mit ausführlicher Ausgabe
	"""
	global CANCEL_INSTALLATION

	print(f"\n[{get_timestamp()}] Starte Installation von {package}...")
	print("=" * 70)

	# Befehl für die Installation
	cmd = [sys.executable, "-m", "pip", "install", "--upgrade"]

	# Für PaddleOCR mehr Zeit und detaillierte Ausgabe geben
	timeout = 600  # 10 Minuten Timeout als Standard
	if package == "paddleocr":
		verbose = True
		timeout = 1200  # 20 Minuten für PaddleOCR
		print(f"[{get_timestamp()}] PaddleOCR-Installation kann bis zu 20 Minuten dauern (Modelldownloads)...")
		print(f"[{get_timestamp()}] Zeige vollständige Ausgabe für bessere Fehlerdiagnose.\n")

	# Befehl vervollständigen
	cmd.append(package)

	try:
		# Starte den Prozess
		if verbose:
			# Im ausführlichen Modus: Zeige vollständige Ausgabe
			print(f"[{get_timestamp()}] Ausführung: {' '.join(cmd)}")

			process = subprocess.Popen(
				cmd,
				stdout=subprocess.PIPE,
				stderr=subprocess.STDOUT,
				text=True,
				bufsize=1  # Zeilengepuffert
			)

			# Startzeit für Timeout
			start_time = time.time()

			# Einfacher Timer für Updates selbst wenn keine Ausgabe erfolgt
			last_update = time.time()

			# Ausgabe in Echtzeit anzeigen
			output_lines = []
			while process.poll() is None:
				# Timeout-Prüfung
				if time.time() - start_time > timeout:
					process.terminate()
					print(f"\n[{get_timestamp()}] FEHLER: Timeout nach {timeout} Sekunden!")
					return False

				# Abbruch-Prüfung
				if CANCEL_INSTALLATION:
					process.terminate()
					print(f"\n[{get_timestamp()}] Installation abgebrochen durch Benutzer.")
					return False

				# Zeige regelmäßige Updates, auch wenn keine Ausgabe erfolgt
				if time.time() - last_update > 20:  # Alle 20 Sekunden
					elapsed = int(time.time() - start_time)
					print(f"[{get_timestamp()}] Installation läuft seit {elapsed} Sekunden...")
					last_update = time.time()

				# Lese eine Zeile, wenn verfügbar (non-blocking)
				line = process.stdout.readline()
				if line:
					# Zeile speichern für spätere Analyse
					output_lines.append(line.strip())
					# Zeige die Zeile an
					print(line.strip())
					last_update = time.time()
				else:
					# Kurze Pause, um CPU-Last zu reduzieren
					time.sleep(0.1)

			# Lese verbleibende Ausgabe
			for line in process.stdout:
				output_lines.append(line.strip())
				print(line.strip())

			# Prüfe Ergebnis
			if process.returncode == 0:
				print(f"\n[{get_timestamp()}] ✅ {package} erfolgreich installiert.")
				return True
			else:
				print(f"\n[{get_timestamp()}] ❌ Fehler bei der Installation von {package}.")
				return False

		else:
			# Im Standard-Modus: Zeige Fortschrittsbalken
			print(f"[{get_timestamp()}] Installiere {package}...")

			process = subprocess.Popen(
				cmd,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True
			)

			# Simuliere Fortschritt während der Installation
			start_time = time.time()
			last_percent = 0

			while process.poll() is None:
				# Timeout-Prüfung
				if time.time() - start_time > timeout:
					process.terminate()
					print(f"\n[{get_timestamp()}] FEHLER: Timeout nach {timeout} Sekunden!")
					return False

				# Abbruch-Prüfung
				if CANCEL_INSTALLATION:
					process.terminate()
					print(f"\n[{get_timestamp()}] Installation abgebrochen durch Benutzer.")
					return False

				# Berechne Fortschritt basierend auf Zeit
				elapsed = time.time() - start_time
				# Maximaler Fortschritt während der Installation ist 95%
				percent = min(95, (elapsed / (timeout * 0.3)) * 100)

				# Nur anzeigen, wenn sich der Prozentsatz ändert
				if int(percent) > last_percent:
					last_percent = int(percent)
					print_progress_bar(percent, prefix=f'[{get_timestamp()}] {package}:',
									   suffix=f'In Bearbeitung...', length=40)

				time.sleep(0.5)

			# Installation abgeschlossen
			stdout, stderr = process.communicate()

			if process.returncode == 0:
				print_progress_bar(100.0, prefix=f'[{get_timestamp()}] {package}:',
								   suffix='✅ Abgeschlossen', length=40)
				return True
			else:
				print_progress_bar(100.0, prefix=f'[{get_timestamp()}] {package}:',
								   suffix='❌ Fehlgeschlagen', length=40)
				print(f"\nFehler bei der Installation von {package}:")
				print(stderr)
				return False

	except Exception as e:
		print(f"\n[{get_timestamp()}] ❌ Ausnahmefehler bei der Installation von {package}: {e}")
		return False


def keyboard_listener():
	"""Thread-Funktion zum Überwachen von Tastatureingaben"""
	global CANCEL_INSTALLATION
	print("\nDrücken Sie 'q' und Enter jederzeit, um die Installation abzubrechen.")

	while not CANCEL_INSTALLATION:
		try:
			if input().lower() == 'q':
				CANCEL_INSTALLATION = True
				print("\nAbbruch angefordert. Warte auf Beendigung der aktuellen Installation...")
		except:
			# Ignoriere Fehler bei der Eingabe
			pass


def install_packages():
	"""Hauptfunktion zur Installation aller Pakete"""
	global CANCEL_INSTALLATION

	# Starte Thread für Tastaturüberwachung
	keyboard_thread = threading.Thread(target=keyboard_listener)
	keyboard_thread.daemon = True  # Thread wird beendet, wenn Hauptprogramm endet
	keyboard_thread.start()

	# Definiere alle Pakete
	basic_packages = [
		"pillow",  # Bildverarbeitung
		"pdf2image",  # PDF-Unterstützung
		"numpy",  # Numerische Berechnungen
		"matplotlib",  # Visualisierung
	]

	ocr_packages = [
		"paddlepaddle",  # PaddlePaddle Framework (zuerst installieren!)
		"paddleocr",  # PaddleOCR-Engine
		"pytesseract"  # Python-Bindings für Tesseract OCR
	]

	print("\n" + "=" * 70)
	print(f"[{get_timestamp()}] INSTALLATION GRUNDLEGENDER ABHÄNGIGKEITEN")
	print("=" * 70)

	# Installiere grundlegende Pakete
	basic_success = []
	for package in basic_packages:
		if CANCEL_INSTALLATION:
			break

		success = install_package(package)
		if success:
			basic_success.append(package)

	print("\n" + "=" * 70)
	print(f"[{get_timestamp()}] Grundlegende Abhängigkeiten: {len(basic_success)}/{len(basic_packages)} erfolgreich.")
	print("=" * 70 + "\n")

	if CANCEL_INSTALLATION:
		print("Installation wurde abgebrochen.")
		return

	print("Möchten Sie auch die OCR-Abhängigkeiten installieren? (j/n)")
	choice = input().lower()

	if choice.startswith('j'):
		print("\n" + "=" * 70)
		print(f"[{get_timestamp()}] INSTALLATION DER OCR-ABHÄNGIGKEITEN")
		print("=" * 70)

		# Installiere OCR-Pakete
		ocr_success = []
		for package in ocr_packages:
			if CANCEL_INSTALLATION:
				break

			# PaddleOCR braucht besondere Behandlung
			if package == "paddleocr":
				print("\n" + "=" * 70)
				print(f"[{get_timestamp()}] INSTALLATION VON PADDLEOCR")
				print("Diese Installation kann mehrere Minuten dauern und lädt große Modelle herunter.")
				print("Die vollständige Ausgabe wird angezeigt, um Fehler besser zu diagnostizieren.")
				print("=" * 70)

			success = install_package(package, verbose=(package == "paddleocr"))
			if success:
				ocr_success.append(package)

			# Alternative Installation für paddlepaddle, wenn nötig
			if package == "paddlepaddle" and not success:
				print(f"\n[{get_timestamp()}] Versuche alternative Installation von paddlepaddle...")
				alt_versions = ["paddlepaddle==2.4.1", "paddlepaddle==2.4.0", "paddlepaddle==2.3.2"]

				for alt_version in alt_versions:
					if CANCEL_INSTALLATION:
						break

					print(f"\n[{get_timestamp()}] Versuche {alt_version}...")
					alt_success = install_package(alt_version)
					if alt_success:
						ocr_success.append("paddlepaddle")
						break

		print("\n" + "=" * 70)
		print(f"[{get_timestamp()}] OCR-Abhängigkeiten: {len(ocr_success)}/{len(ocr_packages)} erfolgreich.")
		print("=" * 70)

	if CANCEL_INSTALLATION:
		print("\nInstallation wurde abgebrochen.")
	else:
		print("\nInstallation abgeschlossen.")

	# Versuche zu importieren, um zu bestätigen, dass die Installation erfolgreich war
	try:
		print("\n" + "=" * 70)
		print(f"[{get_timestamp()}] ÜBERPRÜFUNG DER INSTALLATIONEN")
		print("=" * 70)

		to_check = basic_packages.copy()
		if choice.startswith('j') and not CANCEL_INSTALLATION:
			to_check.extend(ocr_packages)

		# Sonderfall-Mappings für Paketnamen zu Modulnamen
		module_mappings = {
			"pillow": "PIL",
			"pytesseract": "pytesseract",
			"paddlepaddle": "paddle",
			"paddleocr": "paddleocr",
			"numpy": "numpy",
			"matplotlib": "matplotlib",
			"pdf2image": "pdf2image"
		}

		# Überprüfe jedes Paket
		successful_imports = 0
		for package in to_check:
			module_name = module_mappings.get(package, package)
			try:
				__import__(module_name)
				print(f"[{get_timestamp()}] {package} ✅ Erfolgreich importiert")
				successful_imports += 1
			except ImportError as e:
				print(f"[{get_timestamp()}] {package} ❌ Import fehlgeschlagen: {e}")

		# Zeige Gesamtfortschritt bei der Überprüfung an
		print("\n" + "-" * 70)
		print(
			f"[{get_timestamp()}] Überprüfung abgeschlossen: {successful_imports}/{len(to_check)} Module erfolgreich.")

	except Exception as e:
		print(f"[{get_timestamp()}] Fehler bei der Überprüfung: {e}")

	print("=" * 70)
	CANCEL_INSTALLATION = True  # Stoppe den Keyboard-Listener-Thread
	print("\nDrücken Sie Enter zum Beenden...")
	input()


if __name__ == "__main__":
	# Überprüfe, ob das Skript mit Administratorrechten ausgeführt wird (unter Windows)
	if os.name == 'nt':
		try:
			# Versuche, in einen geschützten Ordner zu schreiben
			test_file = "C:\\Windows\\Temp\\test_admin.txt"
			with open(test_file, 'w') as f:
				f.write("Test")
			os.remove(test_file)
		except PermissionError:
			print("WARNUNG: Dieses Skript wird möglicherweise nicht mit Administratorrechten ausgeführt.")
			print("Einige Installationen könnten fehlschlagen.")
			print("Es wird empfohlen, das Skript mit Administratorrechten auszuführen.")
			print("\nMöchten Sie trotzdem fortfahren? (j/n)")
			choice = input().lower()
			if not choice.startswith('j'):
				print("Installation abgebrochen.")
				sys.exit(1)

	try:
		install_packages()
	except KeyboardInterrupt:
		print("\nInstallation durch Benutzer abgebrochen.")
		sys.exit(1)