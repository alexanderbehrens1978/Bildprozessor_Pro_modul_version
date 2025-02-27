import tkinter as tk
from tkinter import filedialog, messagebox
import os
import importlib
import sys

# Versuche, die erforderlichen Module zu importieren
try:
	from PIL import Image
	from pdf2image import convert_from_path
except ImportError:
	# Wenn die Module nicht importiert werden können, wird das in der main.py behandelt
	pass

from utils.path_utils import get_program_path
from utils.poppler_utils import set_poppler_path, install_poppler, show_poppler_url, get_poppler_path
from models.settings import SettingsManager
from ui.menu import create_menu
from ui.image_canvas import create_image_canvas, show_image
from ui.filter_layers import create_layers_ui
from image_processing.filters import apply_filter


class ImageProcessorApp:
	def __init__(self, root):
		self.root = root
		self.root.title(
			"Bildprozessor Pro            Version 1.0        21.02.2025 von Alexander Behrens info@alexanderbehrens.com")

		# Initialize settings
		self.settings_manager = SettingsManager()

		# Initialize image variables
		self.original_image = None
		self.processed_image = None
		self.filename = None

		# Create UI components
		self.create_widgets()
		create_menu(self.root, self)

		# Create filter layers
		self.layer_vars = create_layers_ui(
			self.slider_frame,
			self.update_image,
			self.settings_manager.default_layer_settings
		)

	def create_widgets(self):
		main_frame = tk.Frame(self.root)
		main_frame.pack(fill=tk.BOTH, expand=True)

		# Top frame with labels
		top_frame = tk.Frame(main_frame)
		top_frame.pack(fill=tk.X, padx=10, pady=5)
		self.filename_label = tk.Label(top_frame, text="No image loaded", anchor="w")
		self.filename_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
		self.settings_label = tk.Label(top_frame, text="Settings: " + self.settings_manager.settings_file_name,
									   anchor="e")
		self.settings_label.pack(side=tk.RIGHT)

		# Image preview frame
		preview_frame = tk.Frame(main_frame)
		preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

		# Left canvas (original image)
		left_frame = tk.Frame(preview_frame)
		left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.left_canvas = create_image_canvas(left_frame)

		# Right canvas (processed image)
		right_frame = tk.Frame(preview_frame)
		right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
		self.right_canvas = create_image_canvas(right_frame)

		# Slider frame for filter controls
		self.slider_frame = tk.Frame(main_frame)
		self.slider_frame.pack(fill=tk.X, padx=10, pady=10)

	def load_image(self):
		file_path = filedialog.askopenfilename(
			filetypes=[("Images/PDFs", "*.png *.jpg *.jpeg *.pdf"), ("All Files", "*.*")]
		)
		if file_path:
			try:
				if file_path.lower().endswith(".pdf"):
					current_poppler_path = get_poppler_path(self.settings_manager.poppler_path)
					if not current_poppler_path:
						messagebox.showerror("Error",
											 "Poppler path is not set. Please set the Poppler path in 'Settings'.")
						return
					pages = convert_from_path(file_path, dpi=200, poppler_path=current_poppler_path)
					self.original_image = pages[0]
				else:
					self.original_image = Image.open(file_path).convert("RGB")
				self.filename = os.path.basename(file_path)
				self.filename_label.config(text=self.filename)
				show_image(self.original_image, self.left_canvas)
				self.update_image()
				self.left_canvas.update_idletasks()
				h = self.left_canvas.winfo_height()
				self.right_canvas.config(height=h)
			except Exception as e:
				messagebox.showerror("Error", f"Could not load image: {str(e)}")

	def update_image(self, *args):
		if self.original_image:
			img = self.original_image.copy()
			for enabled_var, filter_var, strength_var in self.layer_vars:
				if enabled_var.get():
					img = apply_filter(img, filter_var.get(), strength_var.get())
			self.processed_image = img
			show_image(img, self.right_canvas)

	def save_image(self):
		if self.processed_image:
			filter_info = []
			for i, (enabled_var, filter_var, strength_var) in enumerate(self.layer_vars):
				if enabled_var.get():
					filter_info.append(f"{i + 1}_{filter_var.get()}_{strength_var.get():.2f}")
			default_name = ""
			if self.filename:
				base = os.path.splitext(self.filename)[0]
				default_name = f"{base}_" + "_".join(filter_info) if filter_info else base
			file_path = filedialog.asksaveasfilename(
				defaultextension=".png",
				filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("All Files", "*.*")],
				title="Save Image",
				initialfile=default_name
			)
			if file_path:
				try:
					self.processed_image.save(file_path)
					messagebox.showinfo("Success", "Image successfully saved.")
				except Exception as e:
					messagebox.showerror("Error", f"Saving failed: {str(e)}")

	def save_settings(self):
		"""Save current settings"""
		filename = self.settings_manager.save_settings(self.layer_vars)
		self.settings_label.config(text="Settings: " + filename)

	def load_settings(self):
		"""Load settings from a file"""
		filename = self.settings_manager.load_settings(self.layer_vars)
		self.settings_label.config(text="Settings: " + filename)
		self.update_image()

	def set_poppler_path(self):
		"""Set the Poppler path"""
		new_path = set_poppler_path(self.root, self.settings_manager.poppler_path)
		if new_path:
			self.settings_manager.poppler_path = new_path

	def install_poppler(self):
		"""Install Poppler"""
		install_poppler(self.root)