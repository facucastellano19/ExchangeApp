import requests
from Data.serializer import serializer
from decimal import Decimal, InvalidOperation

class AccountManager:
    
    API_URL = "https://api.currencyfreaks.com/latest?apikey=ee9a2238783f483daf2ab18b1a2a8477"
    
    def __init__(self, username):
        self.username = username.lower()
        self.serial = serializer()

    def mostrar_resumen(self):
        cuentas = self.serial.load_user_accounts(self.username)
        if not cuentas["accounts"]:
            raise ValueError("No tenés cuentas creadas.")
        return cuentas["accounts"]
    
        
    def obtener_monedas_validas(self):
        try:
            response = requests.get(self.API_URL)
            data = response.json()
            rates = data.get("rates", {})
            monedas = list(rates.keys())
            return monedas
        except Exception:
            raise ConnectionError("No se pudo obtener la lista de monedas válidas.")
        

    def crear_nueva_cuenta(self, moneda):
        moneda = moneda.upper()
        
        if len(moneda) > 11 or not moneda.isalpha():
            raise ValueError(f"La moneda '{moneda}' no es válida.")

        monedas_validas = self.obtener_monedas_validas()
        
        if moneda not in monedas_validas:
            raise ValueError(f"La moneda '{moneda}' no es válida.")

        cuentas_usuario = self.serial.load_user_accounts(self.username)

        for cuenta in cuentas_usuario.get("accounts", []):
            if cuenta["currency"] == moneda:
                raise ValueError(f"Ya existe una cuenta en {moneda}.")

        nueva_cuenta = {"currency": moneda, "amount": Decimal('0.00')}
        cuentas_usuario["accounts"].append(nueva_cuenta)

        self.serial.save_user_accounts(self.username, cuentas_usuario)
        return True


    def depositar(self, moneda, monto_str):
        moneda = moneda.upper()
        
        if moneda != "ARS":
            raise ValueError("Solo se pueden realizar depósitos en ARS.")
        
        try:
            monto = Decimal(monto_str)
        except InvalidOperation:
            raise ValueError("Monto inválido. Ingresá un número válido.")
            
        if monto <= 0:
            raise ValueError("El monto debe ser un número positivo.")
        
        cuentas_usuario = self.serial.load_user_accounts(self.username)

        for cuenta in cuentas_usuario.get("accounts", []):
            if cuenta["currency"] == "ARS":
                monto_actual = Decimal(cuenta["amount"]) 
                cuenta["amount"] = monto_actual + monto
                self.serial.save_user_accounts(self.username, cuentas_usuario)
                return True
        
        raise ValueError("No existe una cuenta en ARS. Primero creala.")
    
    
    def comprar_vender_moneda(self, moneda_origen, moneda_destino, monto_str):
        try:
            monto = Decimal(monto_str)
        except InvalidOperation:
            raise ValueError("El monto ingresado no es válido.")
        
        moneda_origen = moneda_origen.upper()
        moneda_destino = moneda_destino.upper()
        
        if monto <= 0:
            raise ValueError("El monto a transferir debe ser mayor a cero.")
        
        cuentas_usuario = self.serial.load_user_accounts(self.username)

        cuenta_origen = None
        cuenta_destino = None
        
        for cuenta in cuentas_usuario.get("accounts", []):
            if cuenta["currency"] == moneda_origen:
                cuenta_origen = cuenta
            if cuenta["currency"] == moneda_destino:
                cuenta_destino = cuenta
        
        if cuenta_origen is None:
            raise ValueError(f"No tenés cuenta en {moneda_origen}.")
        
        if cuenta_destino is None:
            raise ValueError(f"No tenés cuenta en {moneda_destino}.")
        
        if Decimal(cuenta_origen["amount"]) < monto:
            raise ValueError(f"No tenés suficiente saldo en {moneda_origen}.")

        monto_convertido = self.calcular_conversion(monto, moneda_origen, moneda_destino)
        if monto_convertido is None:
            raise ConnectionError("No se pudo obtener la conversión.")
        
        cuenta_origen["amount"] = Decimal(cuenta_origen["amount"]) - monto
        cuenta_destino["amount"] = Decimal(cuenta_destino["amount"]) + monto_convertido
        
        self.serial.save_user_accounts(self.username, cuentas_usuario)
        
        return True
    
    
    def obtener_cotizaciones(self):
        try:
            response = requests.get(self.API_URL)
            data = response.json()
            return data.get("rates", {})
        except Exception:
            raise ConnectionError("No se pudo obtener las cotizaciones.")     
        
    def calcular_conversion(self, monto, moneda_origen, moneda_destino):
        cotizaciones = self.obtener_cotizaciones()
        if not cotizaciones:
            return None

        try:
            tasa_origen = Decimal(str(cotizaciones[moneda_origen]))
            tasa_destino = Decimal(str(cotizaciones[moneda_destino]))
        except (InvalidOperation, KeyError):
            return None
        
        monto_en_usd = monto / tasa_origen
        monto_convertido = monto_en_usd * tasa_destino
        return monto_convertido
