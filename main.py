from PyQt6 import QtWidgets
from Presentation.menu import LoginDialog  # tu clase LoginDialog basada en PyQt6

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    login = LoginDialog()
    login.show()
    app.exec()
