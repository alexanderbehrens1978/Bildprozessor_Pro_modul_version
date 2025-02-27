import tkinter as tk
from tkinter import ttk


def create_filter_options():
	"""Create the list of available filter options"""
	return [
		"Negativ",
		"Multiplikation",
		"Helligkeit",
		"Kontrast",
		"Schärfen",
		"Weichzeichnen",
		"Graustufen",
		"Sepia",
		"Posterize",
		"Solarize",
		"Kantenerkennung",
		"Emboss",
		"Edge Enhance",
		"Detail",
		"Smooth",
		"Binarize",
		"Gamma Correction",
		"Adaptive Threshold",
		"Color Boost",
		"Custom"
	]


def create_layers_ui(parent, update_callback, default_settings=None):
	"""Create the UI for filter layers with sliders and options"""
	filter_options = create_filter_options()
	layers_frame = tk.Frame(parent)
	layers_frame.pack(fill=tk.X)
	layers_frame.grid_columnconfigure(0, weight=1)  # Empty column on the left for right alignment

	layer_vars = []

	for i in range(5):
		sub_frame = tk.Frame(layers_frame, borderwidth=1, relief=tk.GROOVE)
		sub_frame.grid(row=0, column=i + 1, padx=5, pady=5, sticky="nsew")

		label = tk.Label(sub_frame, text=f"Filter {i + 1}", font=("Arial", 10, "bold"))
		label.grid(row=0, column=0, columnspan=2, pady=(2, 5))

		enabled_var = tk.BooleanVar(value=False)
		chk = tk.Checkbutton(sub_frame, variable=enabled_var, command=update_callback)
		chk.grid(row=1, column=0, sticky="w", padx=5)

		filter_var = tk.StringVar()
		cb = ttk.Combobox(sub_frame, textvariable=filter_var, values=filter_options, state="readonly", width=15)
		cb.current(0)
		cb.grid(row=1, column=1, padx=5, pady=2)
		cb.bind("<<ComboboxSelected>>", update_callback)

		strength_var = tk.DoubleVar(value=1.0)
		slider = tk.Scale(sub_frame, from_=0.0, to=1.0, resolution=0.01, orient=tk.HORIZONTAL,
						  variable=strength_var, command=update_callback, length=150)
		slider.grid(row=2, column=0, columnspan=2, padx=5, pady=(2, 5))

		layer_vars.append((enabled_var, filter_var, strength_var))

	# Apply default settings if provided
	if default_settings:
		for setting in default_settings:
			layer_idx = setting["layer"] - 1
			if layer_idx < len(layer_vars):
				enabled_var, filter_var, strength_var = layer_vars[layer_idx]
				enabled_var.set(setting.get("enabled", False))
				filter_var.set(setting.get("filter", filter_options[0]))
				strength_var.set(setting.get("strength", 1.0))

	return layer_vars