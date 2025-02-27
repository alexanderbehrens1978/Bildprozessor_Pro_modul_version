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
	required_packages = {
		'PIL': 'pillow',
		'pdf2image': 'pdf2image',
		'tkinter': None  # tkinter ist Teil der Standard-Python-Installation
	}

	missing_packages = []

	for module_name, package_name in required_packages.items():
		if package_name is None:
			continue  # Überspringen, wenn kein Paket-Name angegeben ist (z.B. für tkinter)

		try:
			importlib.import_module(module_name)
		except ImportError:
			missing_packages.append((module_name, package_name))

	if not missing_packages:
		return True

	# Zeige Dialog, um fehlende Pakete zu installieren
	return install_missing_packages(missing_packages)


def install_missing_packages(missing_packages):
	"""Installiert die fehlenden Pakete nach Bestätigung durch den Benutzer."""
	if not missing_packages:
		return True

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
								  stdout=subprocess.DEVNULL,
								  stderr=subprocess.DEVNULL)
		except subprocess.CalledProcessError:
			messagebox.showinfo(
				"Pip installieren",
				"Pip wird installiert. Dies kann einen Moment dauern..."
			)
			subprocess.check_call([sys.executable, "-m", "ensurepip", "--default-pip"],
								  stdout=subprocess.DEVNULL)

		# Installiere fehlende Pakete
		progress_window = create_progress_window(package_names)

		for i, (module_name, package_name) in enumerate(missing_packages):
			update_progress(progress_window, f"Installiere {package_name}...", i, len(missing_packages))

			try:
				subprocess.check_call(
					[sys.executable, "-m", "pip", "install", package_name],
					stdout=subprocess.DEVNULL,
					stderr=subprocess.DEVNULL
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


def create_progress_window(packages):
	"""Erstellt ein Fortschrittsfenster für die Paket-Installation."""
	window = tk.Toplevel()
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