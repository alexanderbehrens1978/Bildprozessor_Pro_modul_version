import tkinter as tk
import sys

# Wichtig: Dieser Import muss als erstes stehen, vor allen anderen Imports
# die externe Bibliotheken verwenden
try:
	from utils.package_installer import check_and_install_packages

	# Erstelle ein minimales Root-Fenster für Dialog-Anzeige während der Paket-Installation
	root = tk.Tk()
	root.withdraw()  # Verstecke das Hauptfenster zunächst

	# Überprüfe und installiere fehlende Pakete
	if not check_and_install_packages():
		print("Konnte erforderliche Pakete nicht installieren. Beende Programm...")
		sys.exit(1)

	# Erst nachdem die Pakete installiert wurden, importieren wir die Anwendung
	from ui.main_window import ImageProcessorApp

	if __name__ == "__main__":
		# Zeige das Hauptfenster an
		root.deiconify()
		app = ImageProcessorApp(root)
		root.mainloop()
except ImportError as e:
	print(f"Kritischer Fehler beim Import: {e}")
	print("Stellen Sie sicher, dass zumindest die grundlegenden Python-Pakete installiert sind:")
	print("  pip install tkinter")
	print("  pip install utils")
	sys.exit(1)