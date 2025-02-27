import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from PIL import Image, ImageTk

from ocr.ocr_engine import OCREngine
from ocr.ocr_installer import OCRInstaller


class OCRDialog:
	"""Dialog für die OCR-Funktionalität"""

	def __init__(self, parent, image=None):
		"""
		Initialisiert den OCR-Dialog

		Args:
			parent: Übergeordnetes Tkinter-Fenster
			image: PIL.Image oder None (wird später gesetzt)
		"""
		self.parent = parent
		self.image = image
		self.result_image = None
		self.original_image = None
		self.engine = OCREngine()
		self.installer = OCRInstaller(parent)

		# Sprachoptionen
		self.language_options = {
			"Deutsch": "deu",
			"Englisch": "eng",
			"Französisch": "fra",
			"Italienisch": "ita",
			"Spanisch": "spa",
			"Portugiesisch": "por",
			"Russisch": "rus",
			"Japanisch": "jpn"
		}

		# Dialog erstellen
		self.dialog = tk.Toplevel(parent)
		self.dialog.title("Texterkennung (OCR)")
		self.dialog.geometry("900x600")
		self.dialog.minsize(800, 500)

		# Position des Dialogs
		self.dialog.update_idletasks()
		width = self.dialog.winfo_width()
		height = self.dialog.winfo_height()
		x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
		y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
		self.dialog.geometry(f"{width}x{height}+{x}+{y}")

		self.create_widgets()

		# Wenn ein Bild übergeben wurde, zeige es an
		if image:
			self.set_image(image)

	def create_widgets(self):
		"""Erstellt die UI-Elemente für den Dialog"""
		main_frame = ttk.Frame(self.dialog)
		main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

		# Toolbar für Steuerelemente
		toolbar = ttk.Frame(main_frame)
		toolbar.pack(fill=tk.X, pady=(0, 10))

		# Engine-Auswahl
		engine_frame = ttk.LabelFrame(toolbar, text="OCR-Engine")
		engine_frame.pack(side=tk.LEFT, padx=5)

		self.engine_var = tk.StringVar(value="tesseract")

		# Überprüfe verfügbare Engines
		available_engines = self.engine.get_available_engines()

		# Tesseract
		self.rb_tesseract = ttk.Radiobutton(
			engine_frame,
			text="Tesseract OCR",
			variable=self.engine_var,
			value=OCREngine.ENGINE_TESSERACT,
			command=self.on_engine_change
		)
		self.rb_tesseract.pack(anchor=tk.W, padx=5, pady=2)

		if OCREngine.ENGINE_TESSERACT not in available_engines:
			self.rb_tesseract.state(['disabled'])
			install_tesseract_btn = ttk.Button(
				engine_frame,
				text="Installieren",
				width=10,
				command=self.on_install_tesseract
			)
			install_tesseract_btn.pack(anchor=tk.W, padx=(20, 5), pady=(0, 2))

		# PaddleOCR (CPU)
		self.rb_paddleocr = ttk.Radiobutton(
			engine_frame,
			text="PaddleOCR (CPU)",
			variable=self.engine_var,
			value=OCREngine.ENGINE_PADDLEOCR,
			command=self.on_engine_change
		)
		self.rb_paddleocr.pack(anchor=tk.W, padx=5, pady=2)

		if OCREngine.ENGINE_PADDLEOCR not in available_engines:
			self.rb_paddleocr.state(['disabled'])
			install_paddleocr_btn = ttk.Button(
				engine_frame,
				text="Installieren",
				width=10,
				command=lambda: self.on_install_paddleocr(False)
			)
			install_paddleocr_btn.pack(anchor=tk.W, padx=(20, 5), pady=(0, 2))

		# PaddleOCR (GPU)
		self.rb_paddleocr_gpu = ttk.Radiobutton(
			engine_frame,
			text="PaddleOCR (GPU)",
			variable=self.engine_var,
			value=OCREngine.ENGINE_PADDLEOCR_GPU,
			command=self.on_engine_change
		)
		self.rb_paddleocr_gpu.pack(anchor=tk.W, padx=5, pady=2)

		if OCREngine.ENGINE_PADDLEOCR_GPU not in available_engines:
			self.rb_paddleocr_gpu.state(['disabled'])
			install_paddleocr_gpu_btn = ttk.Button(
				engine_frame,
				text="Installieren",
				width=10,
				command=lambda: self.on_install_paddleocr(True)
			)
			install_paddleocr_gpu_btn.pack(anchor=tk.W, padx=(20, 5), pady=(0, 2))

		# Sprach-Auswahl
		language_frame = ttk.LabelFrame(toolbar, text="Sprache")
		language_frame.pack(side=tk.LEFT, padx=5)

		self.language_var = tk.StringVar(value="Deutsch")
		language_dropdown = ttk.Combobox(
			language_frame,
			textvariable=self.language_var,
			values=list(self.language_options.keys()),
			state="readonly",
			width=15
		)
		language_dropdown.pack(padx=5, pady=5)
		language_dropdown.bind("<<ComboboxSelected>>", self.on_language_change)

		# Aktionsschaltflächen
		btn_frame = ttk.Frame(toolbar)
		btn_frame.pack(side=tk.RIGHT, padx=5)

		self.scan_btn = ttk.Button(
			btn_frame,
			text="Text erkennen",
			command=self.on_scan_text
		)
		self.scan_btn.pack(side=tk.LEFT, padx=5)

		self.copy_btn = ttk.Button(
			btn_frame,
			text="In Zwischenablage",
			command=self.on_copy_text
		)
		self.copy_btn.pack(side=tk.LEFT, padx=5)
		self.copy_btn.state(['disabled'])

		self.save_btn = ttk.Button(
			btn_frame,
			text="Als Textdatei speichern",
			command=self.on_save_text
		)
		self.save_btn.pack(side=tk.LEFT, padx=5)
		self.save_btn.state(['disabled'])

		# Haupt-Content-Bereich mit Splitter
		content_frame = ttk.Frame(main_frame)
		content_frame.pack(fill=tk.BOTH, expand=True)

		# Splitter (PanedWindow)
		self.paned = ttk.PanedWindow(content_frame, orient=tk.HORIZONTAL)
		self.paned.pack(fill=tk.BOTH, expand=True)

		# Linke Seite - Bild
		self.image_frame = ttk.Frame(self.paned)
		self.paned.add(self.image_frame, weight=1)

		self.img_canvas = tk.Canvas(self.image_frame, bg="white")
		self.img_canvas.pack(fill=tk.BOTH, expand=True)

		self.img_scrollbar_y = ttk.Scrollbar(self.image_frame, orient=tk.VERTICAL, command=self.img_canvas.yview)
		self.img_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)

		self.img_scrollbar_x = ttk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL, command=self.img_canvas.xview)
		self.img_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)

		self.img_canvas.config(yscrollcommand=self.img_scrollbar_y.set, xscrollcommand=self.img_scrollbar_x.set)

		# Rechte Seite - Erkannter Text und Optionen
		self.text_frame = ttk.Frame(self.paned)
		self.paned.add(self.text_frame, weight=1)

		# Ergebnistext-Bereich
		self.text_label = ttk.Label(self.text_frame, text="Erkannter Text:")
		self.text_label.pack(anchor=tk.W, pady=(0, 5))

		self.text_result = scrolledtext.ScrolledText(self.text_frame, wrap=tk.WORD, width=40, height=20)
		self.text_result.pack(fill=tk.BOTH, expand=True)

		# Optionen unter dem Textfeld
		options_frame = ttk.Frame(self.text_frame)
		options_frame.pack(fill=tk.X, pady=5)

		self.show_boxes_var = tk.BooleanVar(value=True)
		self.show_boxes_check = ttk.Checkbutton(
			options_frame,
			text="Fundstellen hervorheben",
			variable=self.show_boxes_var,
			command=self.on_show_boxes_change
		)
		self.show_boxes_check.pack(side=tk.LEFT, padx=5)

		# Status-Leiste
		self.statusbar = ttk.Label(main_frame, text="Bereit.", relief=tk.SUNKEN, anchor=tk.W)
		self.statusbar.pack(fill=tk.X, pady=(5, 0))

		# Setze Anfangszustand
		self.update_engine_selection()

	def update_status(self, message):
		"""Aktualisiert die Statusleiste mit einer Nachricht"""
		self.statusbar.config(text=message)
		self.dialog.update_idletasks()

	def update_engine_selection(self):
		"""Aktualisiert die Engine-Auswahl basierend auf verfügbaren Engines"""
		available_engines = self.engine.get_available_engines()

		if available_engines:
			# Setze die erste verfügbare Engine als aktiv
			self.engine_var.set(available_engines[0])
			self.engine.set_engine(available_engines[0])

			# Aktiviere die entsprechenden Radio-Buttons
			if OCREngine.ENGINE_TESSERACT in available_engines:
				self.rb_tesseract.state(['!disabled'])

			if OCREngine.ENGINE_PADDLEOCR in available_engines:
				self.rb_paddleocr.state(['!disabled'])

			if OCREngine.ENGINE_PADDLEOCR_GPU in available_engines:
				self.rb_paddleocr_gpu.state(['!disabled'])
		else:
			# Keine Engine verfügbar
			messagebox.showinfo(
				"OCR-Engines nicht verfügbar",
				"Es wurden keine OCR-Engines gefunden. Bitte installiere mindestens eine Engine."
			)

	def on_engine_change(self):
		"""Handler für Änderungen der ausgewählten Engine"""
		selected_engine = self.engine_var.get()
		self.engine.set_engine(selected_engine)

		# Aktualisiere die Sprachauswahl für die ausgewählte Engine
		self.on_language_change()

	def on_language_change(self, event=None):
		"""Handler für Änderungen der ausgewählten Sprache"""
		selected_language = self.language_var.get()
		language_code = self.language_options.get(selected_language, "deu")
		self.engine.set_language(language_code)

	def on_show_boxes_change(self):
		"""Handler für Änderungen der Box-Anzeige-Option"""
		if self.result_image and self.original_image:
			if self.show_boxes_var.get():
				self.display_image(self.result_image)
			else:
				self.display_image(self.original_image)

	def on_install_tesseract(self):
		"""Handler für den Installieren-Button von Tesseract"""
		self.installer.install_tesseract()
		# Nach der Installation die verfügbaren Engines aktualisieren
		self.update_engine_selection()

	def on_install_paddleocr(self, with_gpu=False):
		"""Handler für den Installieren-Button von PaddleOCR"""
		self.installer.install_paddleocr(with_gpu)
		# Nach der Installation die verfügbaren Engines aktualisieren
		self.update_engine_selection()

	def on_scan_text(self):
		"""Handler für den Text erkennen-Button"""
		if not self.image:
			messagebox.showinfo("Kein Bild", "Bitte zuerst ein Bild öffnen.")
			return

		self.update_status("Führe Texterkennung durch...")
		self.scan_btn.state(['disabled'])
		self.text_result.delete(1.0, tk.END)

		# OCR asynchron durchführen
		self.engine.process_image(self.image, self.on_ocr_complete)

	def on_ocr_complete(self, results, error):
		"""Callback nach Abschluss der OCR"""
		self.scan_btn.state(['!disabled'])

		if error:
			self.update_status(f"Fehler: {error}")
			messagebox.showerror("OCR-Fehler", error)
			return

		self.update_status("Texterkennung abgeschlossen.")

		if results and 'text' in results:
			# Zeige den Text im Textfeld an
			self.text_result.delete(1.0, tk.END)
			self.text_result.insert(tk.END, results['text'])

			# Aktiviere die Buttons
			self.copy_btn.state(['!disabled'])
			self.save_btn.state(['!disabled'])

			# Zeige das Bild mit Boxen an, wenn gewünscht
			if self.show_boxes_var.get():
				self.original_image = self.image.copy()
				self.result_image = self.engine.draw_results_on_image(self.image)
				self.display_image(self.result_image)
		else:
			messagebox.showinfo("Keine Ergebnisse", "Es wurde kein Text im Bild gefunden.")

	def on_copy_text(self):
		"""Kopiert den erkannten Text in die Zwischenablage"""
		text = self.text_result.get(1.0, tk.END)
		self.dialog.clipboard_clear()
		self.dialog.clipboard_append(text)
		self.update_status("Text in die Zwischenablage kopiert.")

	def on_save_text(self):
		"""Speichert den erkannten Text als Textdatei"""
		from tkinter import filedialog

		text = self.text_result.get(1.0, tk.END)
		if not text.strip():
			messagebox.showinfo("Kein Text", "Es gibt keinen Text zum Speichern.")
			return

		file_path = filedialog.asksaveasfilename(
			defaultextension=".txt",
			filetypes=[("Textdateien", "*.txt"), ("Alle Dateien", "*.*")],
			title="Als Textdatei speichern"
		)

		if file_path:
			try:
				with open(file_path, 'w', encoding='utf-8') as f:
					f.write(text)
				self.update_status(f"Text gespeichert unter: {file_path}")
			except Exception as e:
				messagebox.showerror("Fehler beim Speichern", str(e))

	def set_image(self, image):
		"""Setzt ein neues Bild für die OCR"""
		self.image = image
		self.original_image = image.copy()
		self.result_image = None
		self.display_image(image)

		# Reset Ergebnisse
		self.text_result.delete(1.0, tk.END)
		self.copy_btn.state(['disabled'])
		self.save_btn.state(['disabled'])

	def display_image(self, image):
		"""Zeigt ein Bild im Canvas an"""
		self.img_canvas.delete("all")

		# Skaliere das Bild, wenn es zu groß ist (für Anzeigezwecke)
		canvas_width = self.img_canvas.winfo_width()
		canvas_height = self.img_canvas.winfo_height()

		# Wenn das Canvas noch keine Größe hat (erster Aufruf)
		if canvas_width <= 1:
			canvas_width = 400
		if canvas_height <= 1:
			canvas_height = 400

		# Berechne Skalierungsfaktor
		img_width, img_height = image.size
		scale_width = canvas_width / img_width if img_width > canvas_width else 1
		scale_height = canvas_height / img_height if img_height > canvas_height else 1
		scale = min(scale_width, scale_height)

		if scale < 1:
			display_img = image.copy()
			new_size = (int(img_width * scale), int(img_height * scale))
			display_img.thumbnail(new_size, Image.LANCZOS)
		else:
			display_img = image

		# Konvertiere zu PhotoImage und zeige an
		photo = ImageTk.PhotoImage(display_img)
		self.img_canvas.create_image(10, 10, image=photo, anchor=tk.NW)
		self.img_canvas.image = photo  # Halte eine Referenz, um Garbage Collection zu verhindern

		# Setze Scrollbars
		self.img_canvas.config(scrollregion=(0, 0, img_width, img_height))

	def run(self):
		"""Zeigt den Dialog modal an"""
		self.dialog.transient(self.parent)
		self.dialog.grab_set()
		self.parent.wait_window(self.dialog)