from decimal import Decimal
import sys
import time
from PyQt6.QtWidgets import QApplication,QWidget,QPushButton,QLineEdit,QLabel,QMainWindow,QTableWidgetItem,QDialog,QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QDoubleValidator
from PyQt6 import QtWidgets
from Business.auth import auth, RegisterResult
from Business.account_manager import AccountManager
from screens.ui_MainWindow import Ui_MainWindow
from screens.ui_createAccount import Ui_DialogCreateAccount
from screens.ui_deposit import Ui_DialogDeposit
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
        self.username = username
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.sistema = AccountManager(username)
        
        # Configuracion de la tabla
        self.ui.tableCurrencies.horizontalHeader().setStretchLastSection(True)
        self.ui.tableCurrencies.verticalHeader().setVisible(False)
        self.ui.tableCurrencies.setAlternatingRowColors(True)
        
        self.update_table()
        
        # Conectar botones
        self.ui.btnLogout.clicked.connect(self.logout)
        self.ui.btnDeposit.clicked.connect(self.open_deposit_dialog)
        self.ui.btnCreateAccount.clicked.connect(self.open_create_account_dialog)
                
    def update_table(self):
        self.ui.tableCurrencies.setRowCount(0)
        summary = self.sistema.mostrar_resumen()
        for account in summary:
            row = self.ui.tableCurrencies.rowCount()
            self.ui.tableCurrencies.insertRow(row)
            self.ui.tableCurrencies.setItem(row, 0, QTableWidgetItem(account["currency"]))
            self.ui.tableCurrencies.setItem(row, 1, QTableWidgetItem(str(account["amount"])))
            

    # Funciones de los botones
    def open_deposit_dialog(self):
        self.deposit_dialog = DepositDialog(self.username)
        self.deposit_dialog.exec()
        self.update_table()
        
    def open_create_account_dialog(self):
        self.create_account_dialog = CreateAccountDialog(self.username)
        self.create_account_dialog.exec()
        self.update_table()
        
    def logout(self):
        self.close()
        self.login_dialog = LoginDialog()
        self.login_dialog.exec()
        
class CreateAccountDialog(QtWidgets.QDialog):
    def __init__(self, username):
        super().__init__()
        self.ui = Ui_DialogCreateAccount()
        self.ui.setupUi(self)
        self.account_manager = AccountManager(username)
        
        self.currencies = sorted(self.account_manager.obtener_monedas_validas())       
        self.ui.cbSelectCurrencyCreate.addItems(self.currencies)
        
        self.ui.btnCreateAccount.clicked.connect(self.create_account_clicked)
        
    def create_account_clicked(self):
        currency = self.ui.cbSelectCurrencyCreate.currentText()
        try:
            self.account_manager.crear_nueva_cuenta(currency)
            QMessageBox.information(self, "Cuenta Creada", f"Se ha creado una nueva cuenta en {currency}.")
            self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

class DepositDialog(QtWidgets.QDialog):
    def __init__(self, username):
        super().__init__()
        self.ui = Ui_DialogDeposit()
        self.ui.setupUi(self)
        
        self.account_manager = AccountManager(username)

        # QLineEdit solo numeros positivos
        self.ui.txtDepositArsAmount.setValidator(QDoubleValidator(0.0, 1000000.0, 2))

        # Conectar botones
        self.ui.btnDeposit.clicked.connect(self.accept_deposit)

    def accept_deposit(self):
        currency = self.ui.cbSelectCurrencyDeposit.currentText()
        amount = self.ui.txtDepositArsAmount.text().strip()
        
        if not amount:
            self.ui.labelStatusDeposit.setText("❌ Por favor, ingrese un monto.")
            return
        
        try:
            amount_decimal = Decimal(amount)
            
            reply = QMessageBox.question(self, 
                    'Confirmar Depósito',
                    f"¿Confirma el depósito de {amount} {currency}?",QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.account_manager.depositar(currency, amount_decimal)
                QMessageBox.information(self, "Depósito Exitoso", f"Se han depositado {amount} {currency} en su cuenta.")
                self.accept()
            else:
                return
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
        
           

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