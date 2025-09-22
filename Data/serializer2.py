import json
from decimal import Decimal

class serializer:

    def __init__(self):
        pass

    def save_user_accounts(self, username, obj):
        file_path = f"{username}_accounts.json"
        try:
            with open(file_path, "w") as f:
                json.dump(obj, f, indent=4, default=str) 
        except Exception as e:
            print(f"Error al guardar las cuentas de {username}: {e.args[0]}")

    def load_user_accounts(self, username):
        file_path = f"{username}_accounts.json"
        try:
            with open(file_path, "r") as f:
                text = f.read()
                if len(text) == 0:
                    return {"accounts": []} 
                
                data = json.loads(text)
                for account in data["accounts"]:
                    account["amount"] = Decimal(account["amount"])
                return data
        except Exception as e:
            print(f"Error al cargar las cuentas de {username}: {e.args[0]}")
            return {"accounts": []} 
            
    def save_users(self, obj):
        try:
            users = self.load_users()
            for new_user in obj.get("users", []):
                for usuario in users["users"]:
                    if usuario["username"] == new_user["username"]:
                        raise ValueError(f"Usuario '{new_user['username']}' ya existe")
                users["users"].append(new_user)
            with open("users.json", "w") as f:
                json.dump(users, f, indent=4)
        except Exception as e:
            print(e.args[0])
            raise

    def load_users(self):
        try:
            with open("users.json", "r") as f:
                text = f.read()
                if len(text) == 0:
                    return {"users":[]}
                return json.loads(text)
        except FileNotFoundError:
            return {"users":[]} 
        except Exception as e:
            print(e.args[0])
            return {"users":[]}

    def check_users_file(self):
        try:
            with open("users.json", "r") as f:
                pass
        except FileNotFoundError:
            with open("users.json", "w") as f:
                json.dump({"users":[]}, f, indent=4)