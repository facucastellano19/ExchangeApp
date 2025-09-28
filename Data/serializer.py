from decimal import Decimal
import json

import sqlobject as SO
from sqlobject import SQLObjectNotFound

database = 'mysql://guest:1234@localhost/exchangeApp'

__connection__ = SO.connectionForURI(database)

class users(SO.SQLObject):
    username = SO.StringCol(length=40, varchar=True)
    password = SO.StringCol(length=100, varchar=True)
 
class accounts(SO.SQLObject):
    currency = SO.StringCol(length=3, varchar=True)
    amount = SO.DecimalCol(size=10, precision=2)
    account_user = SO.ForeignKey('users')

class serializer:

    def __init__(self):
        users.createTable(ifNotExists=True)
        accounts.createTable(ifNotExists=True)
        
    def save_monedas(self, monedas):
        try:
            with open("monedas.json", "w") as f:
                json.dump(monedas, f, indent=4)
        except Exception as e:
            print(f"Error al guardar monedas: {e}")

    def load_monedas(self):
        try:
            with open("monedas.json", "r") as f:
                text = f.read()
                if len(text) == 0:
                    return []
                return json.loads(text)
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Error al cargar monedas: {e}")
            return []
        
    def load_users(self):
        salida = {"users":[]}
        for user in users.select():
            salida["users"].append({
                "username": user.username,
                "password": user.password
            })
        return salida
     
    def save_users(self, obj):
        for u in obj.get("users", []):
            try:
                user_obj = users.select(users.q.username == u["username"]).getOne()
                raise ValueError(f"Usuario '{u['username']}' ya existe")
            except SQLObjectNotFound:
                new_user = users(username=u["username"], password=u["password"])   
                accounts(currency="ARS",amount=Decimal('0.00'), account_user=new_user.id)  
        
    # Funciones de cuentas del usuario
    def save_user_accounts(self, username, obj):
        try:
            user_obj = users.select(users.q.username == username).getOne()
        except SQLObjectNotFound:
            raise ValueError(f"Usuario '{username}' no existe")

        for acc in obj.get("accounts", []):
            try:
                account_obj = accounts.select(
                    (accounts.q.currency == acc["currency"]) & 
                    (accounts.q.account_user == user_obj.id)
                ).getOne()
                account_obj.set(amount=acc["amount"])

            except SQLObjectNotFound:
                accounts(
                    currency=acc["currency"],
                    amount=acc["amount"],
                    account_user=user_obj.id
                )             

    def load_user_accounts(self, username):
        try:
            user_obj = users.select(users.q.username == username).getOne()
        except SQLObjectNotFound:
            return {"accounts": []}

        accounts_list = []
        for acc in accounts.select(accounts.q.account_user == user_obj.id):
            accounts_list.append({
                "currency": acc.currency,
                "amount": acc.amount
            })
        return {"accounts": accounts_list}