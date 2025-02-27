import sys
import subprocess
import importlib
import tkinter as tk
from tkinter import messagebox


def check_and_install_packages():
	"""
	Überprüft alle benötigten Pakete und installiert fehlende automatisch.
	Gibt True zurück, wenn alle Pakete verfügbar sind (nach Installation), sonst False.
	"""
	# Grundlegende Pakete, die für die Hauptfunktionalität benötigt werden
	required_packages = {
		'PIL': 'pillow',
		'pdf2image': 'pdf2image',
		'tkinter': None,  # tkinter ist Teil der Standard-Python-Installation
		'numpy': 'numpy',  # für fortgeschrittene Bildverarbeitung
		'matplotlib': 'matplotlib',  # für Histogrammanzeige und andere Visualisierungen
	}

	# OCR-spezifische Pakete - werden separat behandelt, da sie schwieriger zu installieren sind
	ocr_packages = {
		'pytesseract': 'pytesseract',  # Python-Bindings für Tesseract OCR
		'paddle': 'paddlepaddle',  # PaddlePaddle Framework
		'paddleocr': 'paddleocr'  # PaddleOCR-Engine
	}

	# Prüfe und installiere zuerst die grundlegenden Pakete
	missing_packages = check_missing_packages(required_packages)

	if missing_packages:
		success = install_missing_packages(missing_packages)
		if not success:
			return False

	# Informiere über OCR-Pakete, aber versuche nicht, sie automatisch zu installieren
	# (das wird von den spezialisierten OCR-Installationsroutinen gemacht)
	missing_ocr = check_missing_packages(ocr_packages)
	if missing_ocr:
		package_names = [pkg_name for _, pkg_name in missing_ocr]
		package_list = ", ".join(package_names)
		print(f"OCR-Funktionalität: Folgende OCR-Pakete sind nicht installiert: {package_list}")
		print("Diese können bei Bedarf über das OCR-Menü installiert werden.")

	return True


def check_missing_packages(packages_dict):
	"""Überprüft, welche Pakete aus dem Dictionary fehlen"""
	missing_packages = []

	for module_name, package_name in packages_dict.items():
		if package_name is None:
			continue  # Überspringen, wenn kein Paket-Name angegeben ist (z.B. für tkinter)

		try:
			importlib.import_module(module_name)
		except ImportError:
			missing_packages.append((module_name, package_name))

	return missing_packages


def install_missing_packages(missing_packages):
	"""Installiert die fehlenden Pakete nach Bestätigung durch den Benutzer."""
	if not missing_packages:
		return True

	# Root-Fenster für Dialog erstellen
	root = None
	try:
		root = tk.Tk()
		root.withdraw()  # Verstecke das Fenster

		package_names = [pkg_name for _, pkg_name in missing_packages]
		package_list = ", ".join(package_names)

		answer = messagebox.askyesno(
			"Fehlende Pakete",
			f"Die folgenden Pakete sind nicht installiert, werden aber benötigt:\n\n{package_list}\n\n"
			"Sollen diese Pakete jetzt installiert werden?"
		)

		if not answer:
			messagebox.showerror(
				"Fehlende Pakete",
				"Die Anwendung kann ohne die erforderlichen Pakete nicht ausgeführt werden."
			)
			return False

		try:
			# Installiere pip, falls es nicht verfügbar ist
			try:
				subprocess.check_call([sys.executable, "-m", "pip", "--version"],
									  stdout=subprocess.PIPE,
									  stderr=subprocess.PIPE)
			except subprocess.CalledProcessError:
				messagebox.showinfo(
					"Pip installieren",
					"Pip wird installiert. Dies kann einen Moment dauern..."
				)
				subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"],
									  stdout=subprocess.PIPE,
									  stderr=subprocess.PIPE)

			# Installiere fehlende Pakete
			progress_window = create_progress_window(root, package_names)

			for i, (module_name, package_name) in enumerate(missing_packages):
				update_progress(progress_window, f"Installiere {package_name}...", i, len(missing_packages))

				try:
					# Aktualisiere pip, wenn nötig
					if i == 0:
						try:
							subprocess.check_call(
								[sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
								stdout=subprocess.PIPE,
								stderr=subprocess.PIPE
							)
						except:
							# Ignoriere Fehler beim pip-Update
							pass

					# Installiere das Paket
					subprocess.check_call(
						[sys.executable, "-m", "pip", "install", package_name],
						stdout=subprocess.PIPE,
						stderr=subprocess.PIPE
					)

					# Versuche, das Modul nach der Installation zu importieren
					importlib.import_module(module_name)
				except (subprocess.CalledProcessError, ImportError) as e:
					progress_window.destroy()
					messagebox.showerror(
						"Installationsfehler",
						f"Fehler beim Installieren von {package_name}: {str(e)}"
					)
					return False

			progress_window.destroy()
			messagebox.showinfo(
				"Installation abgeschlossen",
				"Alle benötigten Pakete wurden erfolgreich installiert."
			)
			return True

		except Exception as e:
			messagebox.showerror(
				"Installationsfehler",
				f"Ein Fehler ist bei der Installation aufgetreten: {str(e)}"
			)
			return False

	finally:
		if root is not None and root.winfo_exists():
			root.destroy()


def create_progress_window(parent, packages):
	"""Erstellt ein Fortschrittsfenster für die Paket-Installation."""
	window = tk.Toplevel(parent)
	window.title("Pakete werden installiert")
	window.geometry("400x150")
	window.resizable(False, False)

	# Zentriere das Fenster
	window.update_idletasks()
	width = window.winfo_width()
	height = window.winfo_height()
	x = (window.winfo_screenwidth() // 2) - (width // 2)
	y = (window.winfo_screenheight() // 2) - (height // 2)
	window.geometry(f"{width}x{height}+{x}+{y}")

	# Fenster immer im Vordergrund
	window.attributes("-topmost", True)

	tk.Label(
		window,
		text="Installation der benötigten Pakete",
		font=("Arial", 12, "bold")
	).pack(pady=(20, 10))

	# Fortschrittstext
	progress_label = tk.Label(window, text="Initialisiere...", font=("Arial", 10))
	progress_label.pack(pady=5)

	# Fortschrittsbalken
	progress_frame = tk.Frame(window, height=20, width=360, bd=1, relief=tk.SUNKEN)
	progress_frame.pack(pady=10)
	progress_frame.pack_propagate(False)

	progress_bar = tk.Frame(progress_frame, height=18, width=0, bg="#4f81bd")
	progress_bar.place(x=0, y=0)

	window.progress_label = progress_label
	window.progress_bar = progress_bar
	window.total_packages = len(packages)

	return window


def update_progress(window, text, current, total):
	"""Aktualisiert den Fortschritt im Fortschrittsfenster."""
	window.progress_label.config(text=text)
	progress_width = int((current / total) * 358)
	window.progress_bar.config(width=progress_width)
	window.update()