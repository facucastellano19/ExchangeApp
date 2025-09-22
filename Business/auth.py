import bcrypt
from Data.serializer import serializer
from enum import Enum
from decimal import Decimal

class RegisterResult(Enum):
    SUCCESS = 1
    USER_EXISTS = 2
    PASSWORDS_DO_NOT_MATCH = 3
    INVALID_PASSWORD = 4

class auth:
    
    def __init__(self):
        self.serial = serializer()

    def is_valid_password(self, password):
        return (
        8 <= len(password) <= 12 and                  
        any(c.islower() for c in password) and        
        any(c.isupper() for c in password) and        
        any(c.isdigit() for c in password) and        
        not any(c.isspace() for c in password)        
    )

    def login(self, username, password):
        username = username.lower()
        
        users = self.serial.load_users()
        for user in users["users"]:
            if user["username"] == username:
                if bcrypt.checkpw(password.encode(), user["password"].encode()):
                    return True
        return False

    def hashPassword(self, password):
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    
    def register(self, username, password1, password2):
        username = username.lower()

        if password1 != password2:
            return RegisterResult.PASSWORDS_DO_NOT_MATCH

        if not self.is_valid_password(password1):
            return RegisterResult.INVALID_PASSWORD

        hashedPwd = self.hashPassword(password1)
        
        user = {
            "users": [
                {"username": username, "password": hashedPwd}
            ]
        }
        
        try:
            self.serial.save_users(user)
        except ValueError:
            return RegisterResult.USER_EXISTS

        initial_accounts = {
            "accounts": [
                {"currency": "ARS", "amount": Decimal('0.00')}
            ]
        }

        self.serial.save_user_accounts(username, initial_accounts)
        return RegisterResult.SUCCESS


