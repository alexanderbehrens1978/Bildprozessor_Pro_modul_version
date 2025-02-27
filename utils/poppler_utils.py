import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
from utils.path_utils import get_program_path


def set_poppler_path(parent_window, current_path=""):
	"""Dialog to set the Poppler path"""
	prog_path = get_program_path()
	path = filedialog.askdirectory(
		title=r"Select the Poppler-Library-Bin folder",
		initialdir=prog_path
	)
	if path:
		messagebox.showinfo("Poppler Path", f"Poppler path set to:\n{path}")
		return path
	return current_path


def install_poppler(parent_window):
	"""Direkt Poppler installieren, nicht nur einen Link anzeigen"""
	try:
		# Zeige Fortschrittsanzeige
		progress = tk.Toplevel(parent_window)
		progress.title("Poppler Installation")
		progress.geometry("300x100")
		progress.resizable(False, False)

		# Zentriere das Fenster
		progress.update_idletasks()
		width = progress.winfo_width()
		height = progress.winfo_height()
		x = (progress.winfo_screenwidth() // 2) - (width // 2)
		y = (progress.winfo_screenheight() // 2) - (height // 2)
		progress.geometry(f"{width}x{height}+{x}+{y}")

		# Fenster immer im Vordergrund
		progress.attributes("-topmost", True)
		progress.grab_set()  # Modal-Dialog

		# Fortschrittstext
		progress_label = tk.Label(progress, text="Installiere Poppler...", font=("Arial", 10))
		progress_label.pack(pady=20)
		progress.update()

		if sys.platform.startswith("win"):
			# Für Windows: Poppler-Binaries direkt herunterladen und installieren
			try:
				# Versuche zuerst Chocolatey
				subprocess.check_call(["choco", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
				progress_label.config(text="Installiere Poppler mit Chocolatey...")
				progress.update()
				subprocess.check_call(["choco", "install", "poppler", "-y"],
									  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
				progress.destroy()
				messagebox.showinfo("Poppler Installation", "Poppler wurde erfolgreich installiert.")
				return
			except Exception:
				# Wenn Chocolatey nicht verfügbar ist, direkte Installation
				import os
				import tempfile
				import urllib.request
				import zipfile
				import shutil

				progress_label.config(text="Downloade Poppler...")
				progress.update()

				# URL der Poppler-Windows-Binaries
				poppler_url = "https://github.com/oschwartz10612/poppler-windows/releases/download/v23.11.0-0/Release-23.11.0-0.zip"

				# Alternative URLs falls die erste nicht funktioniert
				alternative_urls = [
					"https://github.com/oschwartz10612/poppler-windows/releases/download/v23.07.0-0/Release-23.07.0-0.zip",
					"https://github.com/oschwartz10612/poppler-windows/releases/download/v22.12.0-0/Release-22.12.0-0.zip"
				]

				try:
					# Temporäres Verzeichnis erstellen
					temp_dir = tempfile.mkdtemp()
					zip_path = os.path.join(temp_dir, "poppler.zip")

					# Download mit Fehlerbehandlung
					download_success = False
					download_errors = []

					try:
						progress_label.config(text=f"Downloade Poppler von {poppler_url}...")
						progress.update()
						urllib.request.urlretrieve(poppler_url, zip_path)
						download_success = True
					except Exception as e:
						download_errors.append(f"Hauptlink: {str(e)}")

						# Versuche alternative URLs
						for i, alt_url in enumerate(alternative_urls):
							try:
								progress_label.config(text=f"Versuche alternativen Download {i + 1}...")
								progress.update()
								urllib.request.urlretrieve(alt_url, zip_path)
								download_success = True
								break
							except Exception as e:
								download_errors.append(f"Alternative {i + 1}: {str(e)}")

					if not download_success:
						error_details = "\n".join(download_errors)
						raise Exception(f"Konnte Poppler nicht herunterladen. Fehler:\n{error_details}")

					progress_label.config(text="Entpacke Poppler-Dateien...")
					progress.update()

					# Zip entpacken mit Fehlerbehandlung
					try:
						progress_label.config(text="Entpacke Poppler-Dateien...")
						progress.update()
						with zipfile.ZipFile(zip_path, 'r') as zip_ref:
							# Liste alle Dateien im Archiv
							file_list = zip_ref.namelist()
							progress_label.config(text=f"Gefunden: {len(file_list)} Dateien")
							progress.update()

							# Entpacke Dateien
							zip_ref.extractall(temp_dir)

						# Überprüfe, ob Dateien entpackt wurden
						progress_label.config(text="Prüfe entpackte Dateien...")
						progress.update()
						extracted_files = os.listdir(temp_dir)
						if len(extracted_files) <= 1:  # Nur die ZIP-Datei
							raise Exception(
								f"Keine Dateien entpackt. Inhalt des Temp-Verzeichnisses: {extracted_files}")
					except Exception as e:
						raise Exception(f"Fehler beim Entpacken: {str(e)}")

					# Installationsziel bestimmen (im Programmordner)
					prog_path = get_program_path()
					poppler_dir = os.path.join(prog_path, "poppler_bin")

					# Stelle sicher, dass der Programmordner schreibbar ist
					try:
						if not os.path.exists(prog_path):
							os.makedirs(prog_path)
						# Teste Schreibzugriff
						test_file = os.path.join(prog_path, "write_test.tmp")
						with open(test_file, 'w') as f:
							f.write("test")
						os.remove(test_file)
					except Exception as e:
						# Fallback auf Benutzerverzeichnis, wenn Programmordner nicht schreibbar ist
						user_dir = os.path.expanduser("~")
						poppler_dir = os.path.join(user_dir, "poppler_bin")
						progress_label.config(text=f"Programmordner nicht schreibbar, verwende: {poppler_dir}")
						progress.update()

					# Löschen, falls bereits vorhanden, mit Fehlerbehandlung
					if os.path.exists(poppler_dir):
						try:
							shutil.rmtree(poppler_dir)
						except Exception as e:
							# Falls Löschen fehlschlägt, versuche einen anderen Namen
							poppler_dir = os.path.join(os.path.dirname(poppler_dir),
													   f"poppler_bin_{int(time.time())}")
							progress_label.config(text=f"Verwende alternativen Ordner: {poppler_dir}")
							progress.update()

					# Finde den korrekten Ordner nach dem Entpacken
					# Nach dem Entpacken könnte es einen "Release-x.x.x-x" Ordner geben
					extracted_folders = [f for f in os.listdir(temp_dir)
										 if os.path.isdir(os.path.join(temp_dir, f))]

					poppler_source = None
					for folder in extracted_folders:
						if os.path.exists(os.path.join(temp_dir, folder, "bin")):
							poppler_source = os.path.join(temp_dir, folder)
							break

					# Wenn kein passendes Verzeichnis gefunden wurde, suche nach 'poppler'
					if not poppler_source and os.path.exists(os.path.join(temp_dir, "poppler")):
						poppler_source = os.path.join(temp_dir, "poppler")

					# Wenn immer noch kein Verzeichnis gefunden wurde, nimm das erste
					if not poppler_source and extracted_folders:
						poppler_source = os.path.join(temp_dir, extracted_folders[0])

					if not poppler_source:
						raise Exception("Konnte nach dem Entpacken keinen Poppler-Ordner finden")

					# Debug-Info
					print(f"Extrahierte Ordner: {extracted_folders}")
					print(f"Gefundener Poppler-Quellordner: {poppler_source}")

					# Kopieren der entpackten Dateien in den Programmordner
					shutil.copytree(poppler_source, poppler_dir)

					# Aufräumen
					shutil.rmtree(temp_dir)

					progress.destroy()
					messagebox.showinfo("Poppler Installation",
										"Poppler wurde erfolgreich installiert.\n"
										f"Installationsort: {poppler_dir}")
					return
				except Exception as e:
					progress.destroy()
					messagebox.showerror("Fehler", f"Fehler beim Herunterladen/Installieren von Poppler: {str(e)}")
					return

		elif sys.platform.startswith("linux"):
			progress_label.config(text="Installiere Poppler mit apt-get...")
			progress.update()
			subprocess.check_call(["sudo", "apt-get", "install", "poppler-utils", "-y"],
								  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			progress.destroy()
			messagebox.showinfo("Poppler Installation", "Poppler wurde erfolgreich installiert.")

		elif sys.platform.startswith("darwin"):
			try:
				subprocess.check_call(["brew", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
				progress_label.config(text="Installiere Poppler mit Homebrew...")
				progress.update()
				subprocess.check_call(["brew", "install", "poppler"],
									  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
				progress.destroy()
				messagebox.showinfo("Poppler Installation", "Poppler wurde erfolgreich installiert.")
			except Exception:
				progress.destroy()
				messagebox.showerror("Fehler",
									 "Homebrew ist nicht installiert.\nBitte installiere Homebrew oder installiere Poppler manuell.")

		else:
			progress.destroy()
			messagebox.showerror("Fehler",
								 "Automatische Installation von Poppler wird für dein Betriebssystem nicht unterstützt. Bitte installiere Poppler manuell.")

	except Exception as e:
		try:
			progress.destroy()
		except:
			pass
		messagebox.showerror("Fehler", f"Fehler bei der Installation von Poppler: {str(e)}")


def show_poppler_url(parent_window):
	"""Show a dialog with the Poppler download URL"""
	top = tk.Toplevel(parent_window)
	top.title("Poppler Download URL")
	tk.Label(top,
			 text="Chocolatey is not installed.\nPlease install Chocolatey or install Poppler manually.\nCopy the following link for download:",
			 justify="left").pack(padx=10, pady=10)
	url = "https://github.com/oschwartz10612/poppler-windows/releases/"
	entry = tk.Entry(top, width=60)
	entry.insert(0, url)
	entry.pack(padx=10, pady=5)
	tk.Button(top, text="Close", command=top.destroy).pack(pady=10)


def get_poppler_path(custom_path=""):
	"""Returns the Poppler path based on whether the script is running as an EXE or not"""
	if getattr(sys, 'frozen', False):
		return os.path.join(sys._MEIPASS, "poppler_bin", "bin")
	else:
		auto_path = os.path.join(get_program_path(), "poppler_bin", "bin")
		if os.path.exists(auto_path):
			return auto_path
		if os.path.exists(custom_path):
			return custom_path
		return ""