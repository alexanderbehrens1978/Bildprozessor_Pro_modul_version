import os
import sys
import subprocess
import tempfile
import urllib.request
import shutil


class WindowsOCRInstaller:
	"""Klasse für OCR-Installation unter Windows"""

	@staticmethod
	def install_tesseract(progress_callback=None):
		"""
		Installiert Tesseract OCR unter Windows

		Args:
			progress_callback (function, optional): Funktion zum Aktualisieren des Fortschritts
		"""

		def log(message, progress=None):
			"""Hilfsfunktion für Fortschrittsrückmeldung"""
			if progress_callback:
				progress_callback(message, progress)
			print(message)

		try:
			log("Initiiere Tesseract-Installation unter Windows...", 0.1)

			# Temporäres Verzeichnis erstellen
			temp_dir = tempfile.mkdtemp()
			installer_path = os.path.join(temp_dir, "tesseract-installer.exe")

			# Download-URL für neueste Tesseract-Version
			tesseract_url = "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe"

			log(f"Lade Tesseract-Installer von {tesseract_url} herunter...", 0.3)
			urllib.request.urlretrieve(tesseract_url, installer_path)

			# Installer ausführen
			log("Starte Tesseract-Installation...", 0.5)
			subprocess.call([installer_path, "/SILENT"])

			# Umgebungsvariablen aktualisieren
			log("Konfiguriere Systemumgebung...", 0.7)
			tesseract_path = "C:\\Program Files\\Tesseract-OCR"

			# Aktuellen PATH auslesen und erweitern
			current_path = os.environ.get('PATH', '')
			if tesseract_path not in current_path:
				new_path = f"{current_path};{tesseract_path}"
				os.environ['PATH'] = new_path

				# Systemweiten PATH aktualisieren
				try:
					command = f'setx PATH "{new_path}" /M'
					subprocess.call(command, shell=True)
				except Exception as path_error:
					log(f"Warnung: Konnte Systempfad nicht vollständig aktualisieren: {path_error}")

			# Installiere pytesseract Python-Bibliothek
			log("Installiere pytesseract...", 0.9)
			subprocess.check_call([sys.executable, "-m", "pip", "install", "pytesseract"])

			log("Tesseract-Installation abgeschlossen!", 1.0)

		except Exception as e:
			log(f"Fehler bei der Tesseract-Installation: {e}")
			raise

	@staticmethod
	def install_paddleocr(with_gpu=False, progress_callback=None):
		"""
		Installiert PaddleOCR unter Windows

		Args:
			with_gpu (bool): Installiert GPU-Version, wenn True
			progress_callback (function, optional): Funktion zum Aktualisieren des Fortschritts
		"""

		def log(message, progress=None):
			"""Hilfsfunktion für Fortschrittsrückmeldung"""
			if progress_callback:
				progress_callback(message, progress)
			print(message)

		try:
			log("Initiiere PaddleOCR-Installation...", 0.1)

			# Abhängigkeiten installieren
			dependencies = [
				"numpy", "opencv-python", "Pillow", "pyyaml",
				"shapely", "scikit-image", "tqdm"
			]

			for idx, pkg in enumerate(dependencies):
				log(f"Installiere {pkg}...", 0.2 + (idx * 0.05))
				subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

			# PaddlePaddle-Version auswählen
			paddle_version = "paddlepaddle-gpu" if with_gpu else "paddlepaddle"
			log(f"Installiere {paddle_version}...", 0.6)
			subprocess.check_call([sys.executable, "-m", "pip", "install", paddle_version])

			# PaddleOCR installieren
			log("Installiere PaddleOCR...", 0.8)
			subprocess.check_call([sys.executable, "-m", "pip", "install", "paddleocr"])

			log(f"PaddleOCR ({'GPU' if with_gpu else 'CPU'}-Version) Installation abgeschlossen!", 1.0)

		except Exception as e:
			log(f"Fehler bei der PaddleOCR-Installation: {e}")
			raise