import sys
import os
import dotenv

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QSurfaceFormat

from Player.ui.main_window import MainWindow


def main():
	# Load env
	dotenv.load_dotenv()

	# Define Surface format for openGL use
	fmt = QSurfaceFormat()
	fmt.setRenderableType(QSurfaceFormat.OpenGL)
	fmt.setVersion(3, 3)
	fmt.setProfile(QSurfaceFormat.CoreProfile)
	fmt.setDepthBufferSize(24)
	fmt.setStencilBufferSize(8)
	QSurfaceFormat.setDefaultFormat(fmt.defaultFormat())

	# Set application
	app = QApplication(sys.argv)
	with open(os.path.join(os.getenv("STYLES_PATH"), "main.qss"), 'r') as _style:
		app.setStyleSheet(_style.read())

	# Define window and show
	win = MainWindow()
	win.show()

	# Exit
	sys.exit(app.exec())

if __name__ == "__main__":
	import locale
	locale.setlocale(locale.LC_NUMERIC, 'C')
	main()