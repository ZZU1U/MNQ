from PyQt5.QtWidgets import QApplication
import sys
from app import MNQ


app = QApplication(sys.argv)
win = MNQ()
win.show()
sys.exit(app.exec_())
