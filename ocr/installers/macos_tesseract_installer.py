import os
import sys
import subprocess


class MacOSOCRInstaller:
	"""Klasse für OCR-Installation unter macOS"""

	@staticmethod
	def _check_homebrew():
		"""Prüft, ob Homebrew installiert ist"""
		try:
			subprocess.check_call(["which", "brew"],
								  stdout=subprocess.DEVNULL,
								  stderr=subprocess.DEVNULL)
			return True
		except subprocess.CalledProcessError:
			return False

	@staticmethod
	def install_tesseract(progress_callback=None):
		"""
		Installiert Tesseract OCR unter macOS

		Args:
			progress_callback (function, optional): Funktion zum Aktualisieren des Fortschritts
		"""

		def log(message, progress=None):
			"""Hilfsfunktion für Fortschrittsrückmeldung"""
			if progress_callback:
				progress_callback(message, progress)
			print(message)

		try:
			log("Initiiere Tesseract-Installation unter macOS...", 0.1)

			# Prüfe Homebrew
			if not MacOSOCRInstaller._check_homebrew():
				raise Exception("Homebrew ist nicht installiert. Bitte installieren Sie Homebrew zuerst.")

			log("Homebrew-Installation bestätigt...", 0.3)

			# Tesseract via Homebrew installieren
			log("Installiere Tesseract...", 0.5)
			subprocess.check_call(["brew", "install", "tesseract"])

			# Zusätzliche Sprachdateien
			log("Installiere Tesseract-Sprachdateien...", 0.7)
			subprocess.check_call(["brew", "install", "tesseract-lang"])

			# Python-Bindings installieren
			log("Installiere pytesseract...", 0.9)
			subprocess.check_call([sys.executable, "-m", "pip", "install", "pytesseract"])

			log("Tesseract-Installation abgeschlossen!", 1.0)

		except Exception as e:
			log(f"Fehler bei der Tesseract-Installation: {e}")
			raise

	@staticmethod
	def install_paddleocr(with_gpu=False, progress_callback=None):
		"""
		Installiert PaddleOCR unter macOS

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