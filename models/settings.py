import os
import json
from tkinter import messagebox, filedialog
from utils.path_utils import get_program_path


class SettingsManager:
	"""Handles loading, saving, and managing application settings"""

	def __init__(self):
		self.poppler_path = ""
		self.default_layer_settings = []
		self.settings_file_name = "No settings loaded"
		self.load_default_settings()

	def load_default_settings(self):
		"""Load default settings from settings.json in the program directory"""
		prog_path = get_program_path()
		settings_file = os.path.join(prog_path, "settings.json")

		# Prüfen, ob settings.json existiert, falls nicht, erstelle sie
		if not os.path.exists(settings_file):
			self.create_default_settings_file(settings_file)

		# Versuche die settings.json zu laden
		try:
			with open(settings_file, "r") as f:
				settings = json.load(f)
			self.poppler_path = settings.get("poppler_path", "")
			self.default_layer_settings = settings.get("layers", [])
			self.settings_file_name = os.path.basename(settings_file)
		except Exception as e:
			messagebox.showerror("Error", f"Settings could not be loaded: {str(e)}")
			self.default_layer_settings = []
			self.settings_file_name = "No settings loaded"

	def create_default_settings_file(self, file_path):
		"""Erstellt eine Standard-settings.json mit Grundeinstellungen"""
		try:
			# Stelle sicher, dass der Ordner existiert
			os.makedirs(os.path.dirname(file_path), exist_ok=True)

			# Standard-Einstellungen erstellen
			default_settings = {
				"poppler_path": "",
				"layers": [
					{
						"layer": 1,
						"enabled": True,
						"filter": "Negativ",
						"strength": 0.5
					},
					{
						"layer": 2,
						"enabled": False,
						"filter": "Helligkeit",
						"strength": 0.7
					},
					{
						"layer": 3,
						"enabled": False,
						"filter": "Kontrast",
						"strength": 0.6
					},
					{
						"layer": 4,
						"enabled": False,
						"filter": "Graustufen",
						"strength": 1.0
					},
					{
						"layer": 5,
						"enabled": False,
						"filter": "Schärfen",
						"strength": 0.3
					}
				]
			}

			# Datei schreiben
			with open(file_path, "w") as f:
				json.dump(default_settings, f, indent=4)

			# Erfolg protokollieren
			print(f"Standard-Einstellungsdatei wurde erstellt: {file_path}")

		except Exception as e:
			print(f"Fehler beim Erstellen der Standard-Einstellungsdatei: {str(e)}")

	def save_settings(self, layer_vars):
		"""Save current settings to settings.json"""
		settings = {
			"poppler_path": self.poppler_path,
			"layers": []
		}
		for idx, (enabled_var, filter_var, strength_var) in enumerate(layer_vars):
			settings["layers"].append({
				"layer": idx + 1,
				"enabled": enabled_var.get(),
				"filter": filter_var.get(),
				"strength": strength_var.get()
			})
		prog_path = get_program_path()
		file_path = os.path.join(prog_path, "settings.json")
		try:
			with open(file_path, "w") as f:
				json.dump(settings, f, indent=4)
			self.settings_file_name = os.path.basename(file_path)
			messagebox.showinfo("Success", "Settings successfully saved.")
			return self.settings_file_name
		except Exception as e:
			messagebox.showerror("Error", f"Saving failed: {str(e)}")
			return self.settings_file_name

	def load_settings(self, layer_vars):
		"""Load settings from a user-selected JSON file"""
		prog_path = get_program_path()
		file_path = filedialog.askopenfilename(
			initialdir=prog_path,
			filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
			title="Load Settings"
		)
		if file_path:
			try:
				with open(file_path, 'r') as f:
					settings = json.load(f)
				self.poppler_path = settings.get("poppler_path", "")
				for setting in settings.get("layers", []):
					layer_idx = setting["layer"] - 1
					if layer_idx < len(layer_vars):
						enabled_var, filter_var, strength_var = layer_vars[layer_idx]
						enabled_var.set(setting.get("enabled", False))
						filter_var.set(setting.get("filter", ""))
						strength_var.set(setting.get("strength", 1.0))
				self.settings_file_name = os.path.basename(file_path)
				messagebox.showinfo("Success", "Settings successfully loaded.")
				return self.settings_file_name
			except Exception as e:
				messagebox.showerror("Error", f"Loading failed: {str(e)}")
				return self.settings_file_name
		return self.settings_file_name