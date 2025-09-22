import sys
import time

from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel,QMainWindow,QTableWidgetItem,QDialog,QMessageBox
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from Business.auth import auth, RegisterResult
from Business.account_manager import AccountManager
from screens.ui_login import Ui_DialogLogin


class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_DialogLogin()
        self.ui.setupUi(self)

        self.sistema = auth()
        
        self.ui.btnLogin.clicked.connect(self.login_clicked)
        
    def login_clicked(self):
        username = self.ui.lineEditUsername.text()
        password = self.ui.lineEditPassword.text()

        if username == "" or password == "":
            self.ui.labelStatus.setText("Por favor, complete todos los campos.")
            return
        
        if self.sistema.login(username, password):
            #Abrir la ventana principal
            self.ui.labelStatus.setText("Exito")

        else:
            self.ui.labelStatus.setText("❌ Usuario o contraseña incorrectos.")

