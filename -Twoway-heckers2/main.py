import sys
from QtDialogs import AuthDialog
from PyQt5.QtWidgets import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AuthDialog()
    window.show()
    sys.exit(app.exec_())

