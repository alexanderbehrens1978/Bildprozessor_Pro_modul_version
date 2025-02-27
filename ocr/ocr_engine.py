import os
import sys
import tempfile
import importlib
import threading
import numpy as np
from PIL import Image, ImageDraw
from tkinter import messagebox


class OCREngine:
	"""Hauptklasse für die OCR-Funktionalität, unterstützt verschiedene OCR-Engines"""

	# Konstanten für die OCR-Engines
	ENGINE_TESSERACT = "tesseract"
	ENGINE_PADDLEOCR = "paddleocr"
	ENGINE_PADDLEOCR_GPU = "paddleocr_gpu"

	def __init__(self):
		"""Initialisiert die OCR-Engine"""
		self.current_engine = self.ENGINE_TESSERACT
		self.available_engines = self._detect_available_engines()
		self.tesseract_engine = None
		self.paddleocr_engine = None
		self.language = "deu"  # Standardsprache für Tesseract (Deutsch)
		self.paddleocr_language = "de"  # Standardsprache für PaddleOCR (Deutsch)
		self.last_results = None
		self.processing = False
		self.cancel_processing = False

	def _detect_available_engines(self):
		"""Erkennt, welche OCR-Engines auf dem System verfügbar sind"""
		available = []

		# Überprüfe Tesseract
		try:
			import pytesseract
			pytesseract.get_tesseract_version()
			available.append(self.ENGINE_TESSERACT)
		except (ImportError, Exception):
			pass

		# Überprüfe PaddleOCR
		try:
			import paddleocr
			available.append(self.ENGINE_PADDLEOCR)

			# Überprüfe, ob GPU-Unterstützung vorhanden ist
			try:
				import paddle
				if hasattr(paddle, 'device'):
					if paddle.device.is_compiled_with_cuda():
						available.append(self.ENGINE_PADDLEOCR_GPU)
			except (ImportError, Exception):
				pass

		except ImportError:
			pass

		return available

	def get_available_engines(self):
		"""Gibt die verfügbaren OCR-Engines zurück"""
		# Aktualisieren, falls seit der Initialisierung etwas installiert wurde
		self.available_engines = self._detect_available_engines()
		return self.available_engines

	def set_engine(self, engine_name):
		"""Setzt die zu verwendende OCR-Engine"""
		if engine_name in self.get_available_engines():
			self.current_engine = engine_name
			return True
		return False

	def set_language(self, language, engine=None):
		"""Setzt die Sprache für die OCR-Erkennung"""
		if engine is None or engine == self.ENGINE_TESSERACT:
			self.language = language

		if engine is None or engine in [self.ENGINE_PADDLEOCR, self.ENGINE_PADDLEOCR_GPU]:
			# Mapping von Tesseract-Sprachcodes zu PaddleOCR-Sprachcodes
			paddle_lang_map = {
				"deu": "de",
				"eng": "en",
				"fra": "fr",
				"ita": "it",
				"spa": "es",
				"por": "pt",
				"rus": "ru",
				"ara": "ar",
				"hin": "hi",
				"jpn": "japan",
				"kor": "korean"
			}

			if language in paddle_lang_map:
				self.paddleocr_language = paddle_lang_map[language]
			else:
				# Fallback zu Englisch
				self.paddleocr_language = "en"

	def _init_tesseract(self):
		"""Initialisiert die Tesseract-Engine"""
		if self.tesseract_engine is None:
			try:
				import pytesseract
				self.tesseract_engine = pytesseract
			except ImportError:
				raise Exception("Tesseract (pytesseract) ist nicht installiert")

	def _init_paddleocr(self, use_gpu=False):
		"""Initialisiert die PaddleOCR-Engine"""
		if self.paddleocr_engine is None:
			try:
				from paddleocr import PaddleOCR
				# Reduziere Paddle-Debug-Output
				os.environ['FLAGS_call_stack_level'] = '2'
				self.paddleocr_engine = PaddleOCR(
					use_angle_cls=True,
					lang=self.paddleocr_language,
					use_gpu=use_gpu
				)
			except ImportError:
				raise Exception("PaddleOCR ist nicht installiert")

	def process_image(self, image, callback=None):
		"""
		Verarbeitet ein Bild mit der ausgewählten OCR-Engine

		Args:
			image: PIL.Image oder Dateipfad
			callback: Funktion, die nach Abschluss aufgerufen wird (erhält Ergebnisse)

		Returns:
			Bei synchronem Aufruf (callback=None): Erkannter Text und Ergebnisdaten
			Bei asynchronem Aufruf (callback nicht None): None (Ergebnisse via Callback)
		"""
		if self.processing:
			return None, "OCR-Verarbeitung läuft bereits"

		self.cancel_processing = False

		# Synchroner oder asynchroner Modus
		if callback is None:
			return self._process_image_sync(image)
		else:
			self.processing = True
			threading.Thread(
				target=self._process_image_thread,
				args=(image, callback)
			).start()
			return None

	def _process_image_thread(self, image, callback):
		"""Thread-Funktion für die asynchrone Bildverarbeitung"""
		try:
			result, error = self._process_image_sync(image)
		except Exception as e:
			result, error = None, str(e)
		finally:
			self.processing = False

		if callback:
			callback(result, error)

	def _process_image_sync(self, image):
		"""Synchrone Bildverarbeitung"""
		try:
			# Stelle sicher, dass wir ein PIL-Image haben
			if isinstance(image, str):
				# Es ist ein Dateipfad
				image = Image.open(image)

			if self.current_engine == self.ENGINE_TESSERACT:
				return self._process_with_tesseract(image)
			elif self.current_engine in [self.ENGINE_PADDLEOCR, self.ENGINE_PADDLEOCR_GPU]:
				return self._process_with_paddleocr(image)
			else:
				return None, f"Unbekannte OCR-Engine: {self.current_engine}"

		except Exception as e:
			return None, f"Fehler bei der OCR-Verarbeitung: {str(e)}"

	def _process_with_tesseract(self, image):
		"""Verarbeitet ein Bild mit Tesseract OCR"""
		try:
			self._init_tesseract()

			# Konvertiere zu RGB, falls notwendig
			if image.mode != 'RGB':
				image = image.convert('RGB')

			# OCR durchführen
			config = f"--psm 3 -l {self.language}"
			text = self.tesseract_engine.image_to_string(image, config=config)

			# Hole Boxen für Visualisierung
			boxes = self.tesseract_engine.image_to_data(image, config=config,
														output_type=self.tesseract_engine.Output.DICT)

			# Ergebnisse formatieren
			result = {
				'text': text,
				'boxes': []
			}

			# Boxen in ein einheitliches Format konvertieren
			n_boxes = len(boxes['text'])
			for i in range(n_boxes):
				if int(boxes['conf'][i]) > 0:  # Nur Ergebnisse mit Konfidenz > 0
					x, y, w, h = boxes['left'][i], boxes['top'][i], boxes['width'][i], boxes['height'][i]
					text = boxes['text'][i]
					conf = boxes['conf'][i]
					if text.strip():  # Nur nicht-leere Texte
						result['boxes'].append({
							'box': [x, y, x + w, y + h],
							'text': text,
							'confidence': conf
						})

			self.last_results = result
			return result, None

		except Exception as e:
			return None, f"Tesseract-Fehler: {str(e)}"

	def _process_with_paddleocr(self, image):
		"""Verarbeitet ein Bild mit PaddleOCR"""
		try:
			use_gpu = self.current_engine == self.ENGINE_PADDLEOCR_GPU
			self._init_paddleocr(use_gpu=use_gpu)

			# Konvertiere zu RGB, falls notwendig
			if image.mode != 'RGB':
				image = image.convert('RGB')

			# Temporäres Speichern des Bildes (PaddleOCR bevorzugt Dateipfade)
			with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
				tmp_path = tmp.name
				image.save(tmp_path)

			try:
				# OCR durchführen
				paddle_result = self.paddleocr_engine.ocr(tmp_path, cls=True)

				# Ergebnisse sammeln
				full_text = []
				boxes = []

				# PaddleOCR gibt für jede Seite eine Liste zurück
				if paddle_result and len(paddle_result) > 0:
					for line in paddle_result[0]:
						if len(line) >= 2:  # [[x,y,x,y],[text,confidence]]
							coords = line[0]
							text_conf = line[1]
							text = text_conf[0]
							confidence = text_conf[1]

							if text.strip():
								full_text.append(text)
								boxes.append({
									'box': [
										int(coords[0][0]), int(coords[0][1]),
										int(coords[2][0]), int(coords[2][1])
									],
									'text': text,
									'confidence': float(confidence)
								})

				# Formatiere Ergebnisse
				result = {
					'text': '\n'.join(full_text),
					'boxes': boxes
				}

				self.last_results = result
				return result, None

			finally:
				# Aufräumen - temporäre Datei löschen
				try:
					os.unlink(tmp_path)
				except:
					pass

		except Exception as e:
			return None, f"PaddleOCR-Fehler: {str(e)}"

	def cancel(self):
		"""Bricht die laufende OCR-Verarbeitung ab"""
		self.cancel_processing = True

	def draw_results_on_image(self, image):
		"""
		Zeichnet die OCR-Ergebnisse (Bounding Boxes) auf das Bild

		Args:
			image: PIL.Image oder Dateipfad

		Returns:
			PIL.Image mit eingezeichneten Boxen
		"""
		if self.last_results is None or 'boxes' not in self.last_results:
			return image

		# Stelle sicher, dass wir ein PIL-Image haben
		if isinstance(image, str):
			image = Image.open(image)

		# Erstelle eine Kopie des Bildes
		annotated_image = image.copy().convert('RGB')
		draw = ImageDraw.Draw(annotated_image)

		# Zeichne Boxen und Text
		for item in self.last_results['boxes']:
			box = item['box']
			text = item['text']

			# Zeichne Box
			draw.rectangle(box, outline='red', width=2)

		# Zeichne Label (optional)
		# draw.text((box[0], box[1] - 10), text[:10], fill='red')

		return annotated_image

	def get_last_results(self):
		"""Gibt die Ergebnisse der letzten OCR-Verarbeitung zurück"""
		return self.last_results
