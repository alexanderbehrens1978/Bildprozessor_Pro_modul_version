import sys
import subprocess
import importlib
import os
import tkinter as tk
from tkinter import messagebox


def update_pip():
	"""
	Aktualisiert pip auf die neueste Version

	Returns:
		bool: True, wenn das Update erfolgreich war, False sonst
	"""
	try:
		print("Aktualisiere pip...")
		subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
		print("Pip erfolgreich aktualisiert.")
		return True
	except subprocess.CalledProcessError as e:
		print(f"Fehler beim Pip-Update: {e}")
		return False
	except Exception as e:
		print(f"Unerwarteter Fehler beim Pip-Update: {e}")
		return False


def install_package(package):
	"""
	Installiert ein einzelnes Paket mit pip
	"""
	try:
		subprocess.check_call([sys.executable, "-m", "pip", "install", package])
		return True
	except Exception as e:
		print(f"Fehler bei der Installation von {package}: {e}")
		return False


def check_and_install_module(module_name, package_name=None):
	"""
	Prüft ein Modul und installiert es, falls es fehlt
	"""
	if package_name is None:
		package_name = module_name

	try:
		importlib.import_module(module_name)
		return True
	except ImportError:
		print(f"Installiere {package_name}...")
		return install_package(package_name)


def check_and_install_packages():
	"""
	Installiert alle erforderlichen Pakete für die Anwendung
	"""
	# Zuerst pip aktualisieren
	if not update_pip():
		print("WARNUNG: Pip-Update fehlgeschlagen.")

	# Liste der Module und ihrer entsprechenden Paketnamen
	required_modules = [
		('tkinter', 'tkinter'),  # Tkinter ist in Python Standard-Bibliothek
		('PIL', 'pillow'),
		('pdf2image', 'pdf2image'),
		('numpy', 'numpy'),
		('matplotlib', 'matplotlib'),
		('pytesseract', 'pytesseract'),
		('paddleocr', 'paddleocr'),
		('paddle', 'paddlepaddle')
	]

	# Module installieren
	missing_packages = []
	for module, package in required_modules:
		if not check_and_install_module(module, package):
			missing_packages.append(package)

	# Versuche requirements.txt zu installieren
	try:
		requirements_path = os.path.join(os.path.dirname(__file__), '..', 'requirements.txt')
		if os.path.exists(requirements_path):
			subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
	except Exception as e:
		print(f"Fehler bei der Installation von requirements.txt: {e}")

	# Zeige Fehlerdialog, wenn Pakete nicht installiert werden konnten
	if missing_packages:
		error_msg = "Folgende Pakete konnten nicht installiert werden:\n" + "\n".join(missing_packages)
		messagebox.showerror("Installations-Fehler", error_msg)
		return False

	return True


def main():
	"""
	Testet die Paketinstallation
	"""
	print("Überprüfe und installiere erforderliche Pakete...")
	success = check_and_install_packages()

	if success:
		print("Alle Pakete erfolgreich installiert.")
	else:
		print("Einige Pakete konnten nicht installiert werden.")


if __name__ == "__main__":
	main()