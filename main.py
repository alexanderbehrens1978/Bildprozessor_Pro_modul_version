import tkinter as tk
import sys
from utils.package_installer import check_and_install_packages
from ui.main_window import ImageProcessorApp

if __name__ == "__main__":
	# Erstelle ein minimales Root-Fenster für Dialog-Anzeige während der Paket-Installation
	root = tk.Tk()
	root.withdraw()  # Verstecke das Hauptfenster zunächst

	# Überprüfe und installiere fehlende Pakete
	if not check_and_install_packages():
		# Beende das Programm, wenn Pakete fehlen und nicht installiert werden konnten
		sys.exit(1)

	# Zeige das Hauptfenster an
	root.deiconify()
	app = ImageProcessorApp(root)
	root.mainloop()