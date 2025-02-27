import tkinter as tk
from utils.poppler_utils import set_poppler_path, install_poppler


def create_menu(root, app):
	"""Create the application menu bar"""
	menu_bar = tk.Menu(root)

	file_menu = tk.Menu(menu_bar, tearoff=0)
	file_menu.add_command(label="Load Image", command=app.load_image)
	file_menu.add_command(label="Save Image", command=app.save_image)
	file_menu.add_separator()
	file_menu.add_command(label="Load Settings", command=app.load_settings)
	file_menu.add_command(label="Save Settings", command=app.save_settings)
	file_menu.add_separator()
	file_menu.add_command(label="Exit", command=root.quit)
	menu_bar.add_cascade(label="File", menu=file_menu)

	settings_menu = tk.Menu(menu_bar, tearoff=0)
	settings_menu.add_command(label="Set Poppler Path", command=lambda: app.set_poppler_path())
	settings_menu.add_command(label="Install Poppler", command=lambda: app.install_poppler())
	menu_bar.add_cascade(label="Settings", menu=settings_menu)

	# OCR-Menü
	ocr_menu = tk.Menu(menu_bar, tearoff=0)
	ocr_menu.add_command(label="Texterkennung (OCR)", command=app.show_ocr_dialog)
	ocr_menu.add_separator()
	ocr_menu.add_command(label="Tesseract OCR installieren", command=app.install_tesseract)
	ocr_menu.add_command(label="PaddleOCR (CPU) installieren", command=lambda: app.install_paddleocr(False))
	ocr_menu.add_command(label="PaddleOCR (GPU) installieren", command=lambda: app.install_paddleocr(True))
	menu_bar.add_cascade(label="OCR", menu=ocr_menu)

	# Hilfe-Menü
	help_menu = tk.Menu(menu_bar, tearoff=0)
	help_menu.add_command(label="Über", command=app.show_about)
	menu_bar.add_cascade(label="Hilfe", menu=help_menu)

	root.config(menu=menu_bar)

	return menu_bar