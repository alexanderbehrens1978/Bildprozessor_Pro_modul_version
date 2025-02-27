import tkinter as tk
from PIL import ImageTk


def create_image_canvas(parent):
	"""Create a scrollable canvas for displaying images"""
	frame = tk.Frame(parent)
	frame.pack(fill=tk.BOTH, expand=True)

	canvas = tk.Canvas(frame, bg="white", height=480)
	canvas.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

	scrollbar_y = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
	scrollbar_y.grid(row=0, column=1, sticky="ns")

	scrollbar_x = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
	scrollbar_x.grid(row=1, column=0, sticky="ew")

	canvas.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
	frame.grid_rowconfigure(0, weight=1)
	frame.grid_columnconfigure(0, weight=1)

	return canvas


def show_image(image, canvas):
	"""Display an image on the given canvas"""
	canvas.delete("all")
	photo = ImageTk.PhotoImage(image)
	canvas.create_image(10, 10, image=photo, anchor="nw")
	canvas.image = photo  # Keep a reference to prevent garbage collection
	width, height = image.size
	canvas.config(scrollregion=(0, 0, width + 20, height + 20))