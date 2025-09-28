import sys
import time
from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel,QMainWindow,QTableWidgetItem,QDialog,QMessageBox
from PyQt6.QtCore import Qt
from PyQt6 import QtWidgets
from Business.auth import auth, RegisterResult
from Business.account_manager import AccountManager
from screens.ui_MainWindow import Ui_MainWindow
from screens.ui_login import Ui_DialogLogin
from screens.ui_register import Ui_DialogRegister

class LoginDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        
        #Inicializar la interfaz de usuario
        self.ui = Ui_DialogLogin()
        self.ui.setupUi(self)

        self.sistema = auth()
        
        #Conectar botones a funciones
        self.ui.btnLogin.clicked.connect(self.login_clicked)
        self.ui.btnRegister.clicked.connect(self.register)        
        
    def login_clicked(self):
        username = self.ui.lineEditUsername.text()
        password = self.ui.lineEditPassword.text()

        if username == "" or password == "":
            self.ui.labelStatusLogin.setText("❌ Por favor, complete todos los campos.")
            return
        
        if self.sistema.login(username, password):
            self.mainWindow = MainWindow(username)
            self.mainWindow.show()
            
            self.close()
        else:
            self.ui.labelStatusLogin.setText("❌ Usuario o contraseña incorrectos.")
    
    def register(self):
        self.register_dialog = RegisterDialog()
        self.register_dialog.exec()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.sistema = AccountManager(username)
        
        # Configuracion de la tabla
        self.ui.tableCurrencies.horizontalHeader().setStretchLastSection(True)
        self.ui.tableCurrencies.verticalHeader().setVisible(False)
        self.ui.tableCurrencies.setAlternatingRowColors(True)
        
        # Llenar la tabla con el resumen
        try:
            resumen = self.sistema.mostrar_resumen()
            for cuenta in resumen:
                row = self.ui.tableCurrencies.rowCount()
                self.ui.tableCurrencies.insertRow(row)
                self.ui.tableCurrencies.setItem(row, 0, QTableWidgetItem(cuenta["currency"]))
                self.ui.tableCurrencies.setItem(row, 1, QTableWidgetItem(str(cuenta["amount"])))
        except ValueError as e:
            QMessageBox.warning(self, "Atención", str(e)) 


class RegisterDialog(QtWidgets.QDialog):
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_DialogRegister()
        self.ui.setupUi(self)

        self.sistema = auth()
        
        self.ui.btnRegister.clicked.connect(self.register_clicked)
        
        
    def register_clicked(self):
        username = self.ui.lineEditUsername.text()
        password1 = self.ui.lineEditPassword.text()
        password2 = self.ui.lineEditPassword2.text() 

        if username == "" or password1 == "" or password2 == "":
            self.ui.labelStatusRegister.setText("❌ Por favor, complete todos los campos.")
            return
        
        result = self.sistema.register(username, password1, password2)
        
        if result == RegisterResult.SUCCESS:
            QMessageBox.information(self, "Registro Exitoso", "Usuario registrado exitosamente.")
            self.close()
        elif result == RegisterResult.USER_EXISTS:
            self.ui.labelStatusRegister.setText("❌ El usuario ya existe.")
        elif result == RegisterResult.PASSWORDS_DO_NOT_MATCH:
            self.ui.labelStatusRegister.setText("❌ Las contraseñas no coinciden.")
        elif result == RegisterResult.INVALID_PASSWORD:
            self.ui.labelStatusRegister.setText("❌ La contraseña debe tener entre 8-12 caracteres, mayúsculas y números")