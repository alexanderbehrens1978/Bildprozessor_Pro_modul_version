import os
import sys
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox
import importlib
import tempfile
import urllib.request
import shutil
import threading
from utils.path_utils import get_program_path


class OCRInstaller:
	"""Klasse zum Installieren und Konfigurieren von OCR-Engines"""

	def __init__(self, parent_window):
		self.parent_window = parent_window
		self.progress_window = None
		self.progress_label = None
		self.progress_bar = None
		self.cancel_flag = False

	def check_tesseract(self):
		"""Überprüft, ob Tesseract OCR installiert ist"""
		try:
			# Versuche, tesseract aufzurufen
			result = subprocess.run(
				["tesseract", "--version"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				text=True,
				timeout=5
			)
			return "tesseract" in result.stdout.lower()
		except Exception:
			return False

	def check_pytesseract(self):
		"""Überprüft, ob pytesseract installiert ist"""
		try:
			importlib.import_module('pytesseract')
			return True
		except ImportError:
			return False

	def check_paddleocr(self):
		"""Überprüft, ob PaddleOCR installiert ist"""
		try:
			importlib.import_module('paddleocr')
			return True
		except ImportError:
			return False

	def check_paddle_with_gpu(self):
		"""Überprüft, ob PaddlePaddle mit GPU-Unterstützung installiert ist"""
		try:
			paddle = importlib.import_module('paddle')
			if hasattr(paddle, 'device'):
				return paddle.device.is_compiled_with_cuda()
			else:
				return False
		except (ImportError, AttributeError):
			return False

	def create_progress_window(self, title="OCR-Installation"):
		"""Erstellt ein Fortschrittsfenster für die Installation"""
		self.progress_window = tk.Toplevel(self.parent_window)
		self.progress_window.title(title)
		self.progress_window.geometry("500x200")
		self.progress_window.resizable(False, False)

		# Zentriere das Fenster
		self.progress_window.update_idletasks()
		width = self.progress_window.winfo_width()
		height = self.progress_window.winfo_height()
		x = (self.progress_window.winfo_screenwidth() // 2) - (width // 2)
		y = (self.progress_window.winfo_screenheight() // 2) - (height // 2)
		self.progress_window.geometry(f"{width}x{height}+{x}+{y}")

		# Fenster immer im Vordergrund
		self.progress_window.attributes("-topmost", True)
		self.progress_window.grab_set()  # Modal-Dialog

		# Titel
		tk.Label(
			self.progress_window,
			text="OCR-Software Installation",
			font=("Arial", 14, "bold")
		).pack(pady=(20, 10))

		# Fortschrittstext
		self.progress_label = tk.Label(self.progress_window, text="Initialisiere...", font=("Arial", 10))
		self.progress_label.pack(pady=5)

		# Fortschrittsbalken
		progress_frame = tk.Frame(self.progress_window, height=20, width=460, bd=1, relief=tk.SUNKEN)
		progress_frame.pack(pady=10)
		progress_frame.pack_propagate(False)

		self.progress_bar = tk.Frame(progress_frame, height=18, width=0, bg="#4f81bd")
		self.progress_bar.place(x=0, y=0)

		# Abbrechen-Button
		cancel_button = tk.Button(self.progress_window, text="Abbrechen", command=self.cancel_installation)
		cancel_button.pack(pady=10)

		return self.progress_window

	def update_progress(self, text, progress_percent):
		"""Aktualisiert den Fortschritt im Fenster"""
		if self.progress_window and self.progress_window.winfo_exists():
			self.progress_label.config(text=text)
			progress_width = int(progress_percent * 458)
			self.progress_bar.config(width=progress_width)
			self.progress_window.update()

	def close_progress(self):
		"""Schließt das Fortschrittsfenster"""
		if self.progress_window and self.progress_window.winfo_exists():
			self.progress_window.grab_release()
			self.progress_window.destroy()

	def cancel_installation(self):
		"""Bricht die Installation ab"""
		self.cancel_flag = True
		messagebox.showinfo("Installation abgebrochen", "Die Installation wurde abgebrochen.")
		self.close_progress()

	def install_tesseract(self):
		"""Installiert Tesseract OCR"""
		self.cancel_flag = False

		def install_thread():
			try:
				self.create_progress_window("Tesseract OCR Installation")
				self.update_progress("Prüfe Systemvoraussetzungen...", 0.1)

				# OS Detection
				system = platform.system().lower()

				if system == "windows":
					self.install_tesseract_windows()
				elif system == "linux":
					self.install_tesseract_linux()
				elif system == "darwin":
					self.install_tesseract_mac()
				else:
					raise Exception(f"Unbekanntes Betriebssystem: {system}")

				# Nach erfolgreicher Installation von Tesseract, installiere pytesseract
				if not self.cancel_flag:
					self.update_progress("Installiere Python-Bindung pytesseract...", 0.8)
					try:
						subprocess.check_call(
							[sys.executable, "-m", "pip", "install", "pytesseract"],
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE
						)
					except subprocess.CalledProcessError as e:
						raise Exception(f"Fehler bei der Installation von pytesseract: {e}")

					self.update_progress("Installation abgeschlossen!", 1.0)
					if not self.cancel_flag:
						messagebox.showinfo("Installation erfolgreich",
											"Tesseract OCR wurde erfolgreich installiert!")
			except Exception as e:
				if not self.cancel_flag:
					messagebox.showerror("Fehler bei der Installation",
										 f"Fehler bei der Installation von Tesseract OCR: {str(e)}")
			finally:
				self.close_progress()

		# Starte Installation in einem separaten Thread
		threading.Thread(target=install_thread).start()

	def install_tesseract_windows(self):
		"""Installiert Tesseract OCR unter Windows"""
		self.update_progress("Downloade Tesseract Installer...", 0.2)

		if self.cancel_flag:
			return

		# Windows-spezifischer Installer
		temp_dir = tempfile.mkdtemp()
		installer_path = os.path.join(temp_dir, "tesseract-installer.exe")

		try:
			# Download des Installers
			tesseract_url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe"
			self.update_progress(f"Downloade Installer von {tesseract_url}", 0.3)
			urllib.request.urlretrieve(tesseract_url, installer_path)

			if self.cancel_flag:
				return

			# Ausführen des Installers
			self.update_progress("Starte Installation (folge den Anweisungen im Installer)...", 0.4)
			self.progress_window.withdraw()  # Verstecke Fortschrittsfenster während des Installers

			# Führe Installer aus und warte auf Abschluss
			try:
				subprocess.call([installer_path, "/SILENT"])
			except Exception as e:
				raise Exception(f"Fehler beim Ausführen des Installers: {e}")

			self.progress_window.deiconify()  # Zeige Fortschrittsfenster wieder an
			self.update_progress("Konfiguriere Umgebungsvariablen...", 0.7)

			# Setze Umgebungsvariable für den aktuellen Prozess
			os.environ["PATH"] = os.environ["PATH"] + ";C:\\Program Files\\Tesseract-OCR"

			# Versuche, Tesseract zur Windows PATH-Umgebungsvariable hinzuzufügen
			try:
				# Aktuellen PATH auslesen
				command = 'powershell -command "[Environment]::GetEnvironmentVariable(\'PATH\', \'Machine\')"'
				current_path = subprocess.check_output(command, shell=True).decode().strip()

				if "Tesseract-OCR" not in current_path:
					# PATH ergänzen
					new_path = current_path + ";C:\\Program Files\\Tesseract-OCR"
					command = f'powershell -command "[Environment]::SetEnvironmentVariable(\'PATH\', \'{new_path}\', \'Machine\')"'
					subprocess.call(command, shell=True)
			except Exception as e:
				# Wenn es fehlschlägt, melde es, aber breche nicht ab
				print(f"Warnung: Konnte PATH nicht aktualisieren: {str(e)}")

		finally:
			# Aufräumen
			try:
				shutil.rmtree(temp_dir)
			except Exception:
				pass

	def install_tesseract_linux(self):
		"""Installiert Tesseract OCR unter Linux"""
		self.update_progress("Installiere Tesseract via apt...", 0.3)

		if self.cancel_flag:
			return

		# Teste verschiedene Paketmanager
		if self._check_command_exists("apt"):
			# Debian/Ubuntu
			try:
				subprocess.check_call(
					["sudo", "apt-get", "update"],
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE
				)
				self.update_progress("Installiere Tesseract OCR...", 0.5)
				subprocess.check_call(
					["sudo", "apt-get", "install", "-y", "tesseract-ocr", "libtesseract-dev"],
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE
				)
			except subprocess.CalledProcessError as e:
				raise Exception(f"Fehler bei der apt-Installation: {e}")
		elif self._check_command_exists("dnf"):
			# Fedora
			try:
				self.update_progress("Installiere Tesseract via dnf...", 0.5)
				subprocess.check_call(
					["sudo", "dnf", "install", "-y", "tesseract", "tesseract-devel"],
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE
				)
			except subprocess.CalledProcessError as e:
				raise Exception(f"Fehler bei der dnf-Installation: {e}")
		elif self._check_command_exists("pacman"):
			# Arch Linux
			try:
				self.update_progress("Installiere Tesseract via pacman...", 0.5)
				subprocess.check_call(
					["sudo", "pacman", "-S", "--noconfirm", "tesseract", "tesseract-data-eng"],
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE
				)
			except subprocess.CalledProcessError as e:
				raise Exception(f"Fehler bei der pacman-Installation: {e}")
		else:
			raise Exception("Kein unterstützter Paketmanager gefunden (apt, dnf, pacman)")

	def install_tesseract_mac(self):
		"""Installiert Tesseract OCR unter macOS"""
		self.update_progress("Prüfe auf Homebrew...", 0.2)

		if self.cancel_flag:
			return

		# Überprüfe, ob Homebrew installiert ist
		if not self._check_command_exists("brew"):
			raise Exception("Homebrew ist nicht installiert. Bitte installiere Homebrew zuerst: https://brew.sh")

		# Installiere Tesseract via Homebrew
		try:
			self.update_progress("Installiere Tesseract via Homebrew...", 0.4)
			subprocess.check_call(
				["brew", "install", "tesseract"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)

			# Installiere Englische Sprachdateien
			self.update_progress("Installiere Sprachdateien...", 0.6)
			subprocess.check_call(
				["brew", "install", "tesseract-lang"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
		except subprocess.CalledProcessError as e:
			raise Exception(f"Fehler bei der Homebrew-Installation: {e}")

	def install_paddleocr(self, with_gpu=False):
		"""Installiert PaddleOCR mit oder ohne GPU-Unterstützung"""
		self.cancel_flag = False

		def install_thread():
			# Sicherstellen, dass with_gpu im Thread-Kontext verfügbar ist
			nonlocal with_gpu

			try:
				self.create_progress_window("PaddleOCR Installation")
				self.update_progress("Initialisiere...", 0.1)

				# OS Detection
				system = platform.system().lower()

				# Überprüfen, ob Python-Version kompatibel ist
				py_version = sys.version_info
				if py_version.major != 3 or py_version.minor < 7 or py_version.minor > 10:
					messagebox.showwarning(
						"Python-Version nicht optimal",
						"PaddleOCR läuft am besten mit Python 3.7-3.10. " +
						f"Deine Version ist {py_version.major}.{py_version.minor}. " +
						"Die Installation wird fortgesetzt, aber es könnte Probleme geben."
					)

				# Installiere Abhängigkeiten
				self.update_progress("Installiere grundlegende Abhängigkeiten...", 0.2)
				pip_packages = [
					"numpy", "opencv-python", "Pillow", "pyyaml",
					"shapely", "scikit-image", "tqdm"
				]
				for i, pkg in enumerate(pip_packages):
					if self.cancel_flag:
						return
					progress = 0.2 + ((i / len(pip_packages)) * 0.2)
					self.update_progress(f"Installiere {pkg}...", progress)
					try:
						subprocess.check_call(
							[sys.executable, "-m", "pip", "install", pkg],
							stdout=subprocess.PIPE,
							stderr=subprocess.PIPE
						)
					except subprocess.CalledProcessError as e:
						raise Exception(f"Fehler bei der Installation von {pkg}: {e}")

				# Installiere PaddlePaddle zuerst
				# Wichtig: PaddlePaddle muss VOR PaddleOCR installiert werden
				self.update_progress("Vorbereitung für PaddlePaddle...", 0.4)

				# Flag für GPU-Unterstützung
				use_gpu = with_gpu  # Lokale Kopie erstellen

				# Bestimme die korrekte PaddlePaddle-Version
				paddle_version = "paddlepaddle"
				if use_gpu:
					self.update_progress("Prüfe CUDA-Installation...", 0.45)
					cuda_available = self._check_cuda_available()

					if not cuda_available:
						if messagebox.askyesno(
								"CUDA nicht gefunden",
								"CUDA scheint nicht verfügbar zu sein. Möchtest du trotzdem " +
								"versuchen, PaddlePaddle mit GPU-Unterstützung zu installieren?"
						):
							paddle_version = "paddlepaddle-gpu"
						else:
							# Wechsle zur CPU-Version
							paddle_version = "paddlepaddle"
							use_gpu = False  # Update lokale Kopie
					else:
						paddle_version = "paddlepaddle-gpu"

				# Installiere PaddlePaddle
				self.update_progress(f"Installiere {paddle_version}...", 0.5)
				try:
					subprocess.check_call(
						[sys.executable, "-m", "pip", "install", paddle_version],
						stdout=subprocess.PIPE,
						stderr=subprocess.PIPE
					)
				except subprocess.CalledProcessError as e:
					raise Exception(f"Fehler bei der Installation von {paddle_version}: {e}")

				# Überprüfe, ob PaddlePaddle korrekt installiert wurde
				self.update_progress("Überprüfe PaddlePaddle-Installation...", 0.6)
				try:
					# Versuche, paddle zu importieren
					subprocess.check_call(
						[sys.executable, "-c", "import paddle; print('PaddlePaddle OK')"],
						stdout=subprocess.PIPE,
						stderr=subprocess.PIPE
					)
				except subprocess.CalledProcessError as e:
					raise Exception(f"PaddlePaddle-Installation konnte nicht verifiziert werden: {e}")

				# Installiere PaddleOCR
				self.update_progress("Installiere PaddleOCR...", 0.7)
				try:
					subprocess.check_call(
						[sys.executable, "-m", "pip", "install", "paddleocr"],
						stdout=subprocess.PIPE,
						stderr=subprocess.PIPE
					)
				except subprocess.CalledProcessError as e:
					raise Exception(f"Fehler bei der Installation von paddleocr: {e}")

				# Überprüfe, ob PaddleOCR korrekt installiert wurde
				self.update_progress("Überprüfe PaddleOCR-Installation...", 0.8)
				try:
					subprocess.check_call(
						[sys.executable, "-c", "import paddleocr; print('PaddleOCR OK')"],
						stdout=subprocess.PIPE,
						stderr=subprocess.PIPE
					)
				except subprocess.CalledProcessError as e:
					raise Exception(f"PaddleOCR-Installation konnte nicht verifiziert werden: {e}")

				# Lade Sprachmodelle
				self.update_progress("Lade Sprachmodelle...", 0.9)
				try:
					# Vereinfachter Code zum Testen der PaddleOCR-Initialisierung
					test_code = """
import os
os.environ['FLAGS_call_stack_level'] = '2'
import paddleocr
print('PaddleOCR imported successfully')
"""
					subprocess.run(
						[sys.executable, "-c", test_code],
						check=True,
						stdout=subprocess.PIPE,
						stderr=subprocess.PIPE,
						text=True,
						timeout=30
					)
				except Exception as e:
					# Nur warnen, nicht abbrechen
					print(f"Warnung: PaddleOCR-Test fehlgeschlagen, wird später initialisiert: {e}")

				self.update_progress("Installation abgeschlossen!", 1.0)

				if not self.cancel_flag:
					if use_gpu and paddle_version == "paddlepaddle-gpu":
						messagebox.showinfo(
							"Installation erfolgreich",
							"PaddleOCR mit GPU-Unterstützung wurde erfolgreich installiert!"
						)
					else:
						messagebox.showinfo(
							"Installation erfolgreich",
							"PaddleOCR (CPU-Version) wurde erfolgreich installiert!"
						)

			except Exception as e:
				if not self.cancel_flag:
					error_msg = str(e)
					messagebox.showerror(
						"Fehler bei der Installation",
						f"Fehler bei der Installation von PaddleOCR: {error_msg}\n\n"
						"Tipp: Versuchen Sie, die Bibliotheken manuell zu installieren mit:\n"
						"pip install paddlepaddle\n"
						"pip install paddleocr"
					)
			finally:
				self.close_progress()

		# Starte Installation in einem separaten Thread
		threading.Thread(target=install_thread).start()

	def _check_command_exists(self, command):
		"""Überprüft, ob ein Befehl auf dem System existiert"""
		try:
			subprocess.check_call(
				[command, "--version"],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE
			)
			return True
		except (subprocess.CalledProcessError, FileNotFoundError):
			return False

	def _check_cuda_available(self):
		"""Überprüft, ob CUDA auf dem System verfügbar ist"""
		system = platform.system().lower()

		if system == "windows":
			# Prüfe auf CUDA-Installationsverzeichnis unter Windows
			cuda_paths = [
				"C:\\Program Files\\NVIDIA GPU Computing Toolkit\\CUDA",
				"C:\\CUDA"
			]
			for path in cuda_paths:
				if os.path.exists(path):
					return True

			# Prüfe über nvidia-smi
			try:
				subprocess.check_call(
					["nvidia-smi"],
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE
				)
				return True
			except (subprocess.CalledProcessError, FileNotFoundError):
				return False

		elif system == "linux" or system == "darwin":
			# Prüfe über nvidia-smi
			try:
				subprocess.check_call(
					["nvidia-smi"],
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE
				)
				return True
			except (subprocess.CalledProcessError, FileNotFoundError):
				# Prüfe auf CUDA Bibliotheken
				cuda_lib_paths = [
					"/usr/local/cuda/lib64",
					"/usr/lib/cuda",
					"/usr/lib/x86_64-linux-gnu/libcuda.so"
				]
				for path in cuda_lib_paths:
					if os.path.exists(path):
						return True

		return False