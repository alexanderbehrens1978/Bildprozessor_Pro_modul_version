import os
import sys
import subprocess


class LinuxOCRInstaller:
	"""Klasse für OCR-Installation unter Linux"""

	@staticmethod
	def _detect_package_manager():
		"""Erkennt den Paketmanager"""
		if subprocess.call(["which", "apt-get"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
			return "apt"
		elif subprocess.call(["which", "dnf"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
			return "dnf"
		elif subprocess.call(["which", "pacman"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
			return "pacman"
		return None

	@staticmethod
	def install_tesseract(progress_callback=None):
		"""
		Installiert Tesseract OCR unter Linux

		Args:
			progress_callback (function, optional): Funktion zum Aktualisieren des Fortschritts
		"""

		def log(message, progress=None):
			"""Hilfsfunktion für Fortschrittsrückmeldung"""
			if progress_callback:
				progress_callback(message, progress)
			print(message)

		try:
			log("Initiiere Tesseract-Installation unter Linux...", 0.1)

			# Paketmanager ermitteln
			pkg_manager = LinuxOCRInstaller._detect_package_manager()

			if not pkg_manager:
				raise Exception("Kein unterstützter Paketmanager gefunden")

			log(f"Erkannter Paketmanager: {pkg_manager}", 0.3)

			# Installation mit entsprechendem Paketmanager
			if pkg_manager == "apt":
				# Debian/Ubuntu
				subprocess.check_call(["sudo", "apt-get", "update"])
				log("Aktualisiere Paketliste...", 0.4)
				subprocess.check_call(["sudo", "apt-get", "install", "-y", "tesseract-ocr", "libtesseract-dev"])
			elif pkg_manager == "dnf":
				# Fedora
				subprocess.check_call(["sudo", "dnf", "install", "-y", "tesseract", "tesseract-devel"])
			elif pkg_manager == "pacman":
				# Arch Linux
				subprocess.check_call(["sudo", "pacman", "-S", "--noconfirm", "tesseract", "tesseract-data-eng"])

			log("Tesseract-Systempaket installiert...", 0.6)

			# Python-Bindings installieren
			log("Installiere pytesseract...", 0.8)
			subprocess.check_call([sys.executable, "-m", "pip", "install", "pytesseract"])

			log("Tesseract-Installation abgeschlossen!", 1.0)

		except Exception as e:
			log(f"Fehler bei der Tesseract-Installation: {e}")
			raise

	@staticmethod
	def install_paddleocr(with_gpu=False, progress_callback=None):
		"""
		Installiert PaddleOCR unter Linux

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