"""
Einfaches, direktes Installationsskript ohne komplexe Funktionen.
Verwendet nur direkte pip-Befehle.
"""

import subprocess
import sys
import os


def run_pip_install(package):
	"""Führt pip install für ein Paket aus und zeigt die vollständige Ausgabe"""
	print(f"\n{'=' * 70}")
	print(f"INSTALLATION VON: {package}")
	print(f"{'=' * 70}")

	# Direkte Ausführung des pip-Befehls
	command = [sys.executable, "-m", "pip", "install", package]
	print(f"Ausführung: {' '.join(command)}")

	# Diese Methode leitet die Ausgabe direkt an die Konsole weiter
	result = subprocess.call(command)

	if result == 0:
		print(f"\n✅ {package} erfolgreich installiert!")
	else:
		print(f"\n❌ Fehler bei der Installation von {package}!")

	return result == 0


def main_menu():
	"""Zeigt das Hauptmenü an"""
	print("\n" + "=" * 70)
	print("EINFACHER ABHÄNGIGKEITEN-INSTALLER")
	print("=" * 70)
	print("\nWählen Sie eine Option:")
	print("1. Grundlegende Abhängigkeiten installieren (pillow, numpy, pdf2image, matplotlib)")
	print("2. OCR-Abhängigkeiten installieren (pytesseract, paddlepaddle, paddleocr)")
	print("3. Einzelnes Paket installieren")
	print("4. Beenden")

	choice = input("\nIhre Wahl (1-4): ")

	if choice == "1":
		install_basic_dependencies()
	elif choice == "2":
		install_ocr_dependencies()
	elif choice == "3":
		package = input("\nWelches Paket möchten Sie installieren? ")
		if package.strip():
			run_pip_install(package.strip())
	elif choice == "4":
		print("\nProgramm wird beendet.")
		return False
	else:
		print("\nUngültige Auswahl. Bitte versuchen Sie es erneut.")

	return True


def install_basic_dependencies():
	"""Installiert grundlegende Abhängigkeiten"""
	basic_packages = [
		"pillow",
		"numpy",
		"pdf2image",
		"matplotlib"
	]

	success_count = 0
	for package in basic_packages:
		if run_pip_install(package):
			success_count += 1

	print(f"\nGrundlegende Abhängigkeiten: {success_count}/{len(basic_packages)} erfolgreich installiert.")


def install_ocr_dependencies():
	"""Installiert OCR-Abhängigkeiten"""
	ocr_packages = [
		"pytesseract",
		"paddlepaddle",
		"paddleocr"
	]

	print("\nWARNUNG: Die Installation von paddleocr kann sehr lange dauern!")
	print("Es werden große Modelle heruntergeladen und installiert.")
	confirm = input("Fortfahren? (j/n): ")

	if confirm.lower().startswith('j'):
		success_count = 0
		for package in ocr_packages:
			if run_pip_install(package):
				success_count += 1

		print(f"\nOCR-Abhängigkeiten: {success_count}/{len(ocr_packages)} erfolgreich installiert.")
	else:
		print("\nOCR-Installation abgebrochen.")


if __name__ == "__main__":
	# Prüfe Administrator-Rechte auf Windows
	if os.name == 'nt':
		try:
			test_file = "C:\\Windows\\Temp\\test_admin.txt"
			with open(test_file, 'w') as f:
				f.write("Test")
			os.remove(test_file)
			print("Administrator-Rechte: OK")
		except PermissionError:
			print("WARNUNG: Dieses Skript wird nicht mit Administratorrechten ausgeführt.")
			print("Einige Installationen koennten fehlschlagen.")

	# Hauptschleife
	while main_menu():
		input("\nDrücken Sie Enter, um zum Hauptmenü zurückzukehren...")

	input("\nDrücken Sie Enter zum Beenden...")