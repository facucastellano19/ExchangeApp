import sys
import maskpass
import time

from Business.auth import auth, RegisterResult
from Business.account_manager import AccountManager


def mostrar_menu_cuentas(username):

    account_manager = AccountManager(username) 

    while True:
        print(f"\n--- Menú de Cuentas para {username.upper()} ---")
        print("1. Ver Resumen de Cuentas")
        print("2. Crear Nueva Cuenta")
        print("3. Depositar")
        print("4. Comprar/Vender Moneda")
        print("5. Cerrar Sesión") 
        print("6. Salir de la Aplicación")
        print("------------------------------------")
        
        opcion_cuenta = input("Elige una opción: ")
        
        try:
            if opcion_cuenta == "1":
                cuentas = account_manager.mostrar_resumen()
                print("\n📊 Resumen de cuentas:")
                for cuenta in cuentas:
                    print(f"💰 {cuenta['currency']}: {cuenta['amount']}")
                
            elif opcion_cuenta == "2":
                moneda = input("Ingresa la moneda a crear (ej: USD): ").strip()
                if account_manager.crear_nueva_cuenta(moneda):
                    print(f"✅ Cuenta en {moneda.upper()} creada exitosamente.")
                
            elif opcion_cuenta == "3":
                moneda = input("Ingresa la moneda donde deseas depositar (solo ARS): ").strip()
                monto = input("Ingresa el monto a depositar: ").strip()
                if account_manager.depositar(moneda, monto):
                    print(f"✅ Depósito de {monto} {moneda.upper()} realizado con éxito.")
                
            elif opcion_cuenta == "4":
                tinicio = time.time()
                moneda_origen = input("Moneda origen (ej: ARS): ").strip().upper()
                moneda_destino = input("Moneda destino (ej: USD): ").strip().upper()
                monto_str = input(f"Monto a convertir de {moneda_origen} a {moneda_destino}: ").strip()

                response = input("Desea confirmar la operación (S/N)\n")

                if (time.time() - tinicio) > 120:
                    response = 'N'
                
                if response in ('s','S'):
                    if account_manager.comprar_vender_moneda(moneda_origen, moneda_destino, monto_str):
                        print(f"✅ Operación realizada: {monto_str} {moneda_origen} convertidos correctamente a {moneda_destino}")
                else:
                    print("❌ No se pudo completar la operación.")
                
            elif opcion_cuenta == "5":
                print("Cerrando sesión...")
                break

            elif opcion_cuenta == "6":
                print("Saliendo de la aplicación...")
                sys.exit()

            else:
                print("❌ Opción inválida. Por favor, ingresa un número del 1 al 6.")   
        except Exception as e:
            print(f"⚠️  {e}")

        input("\nPresioná Enter para volver al menú...")


def main_app_loop():
    sistema = auth()

    while True:
        print("\n=== Menú de Autenticación ===")
        print("1. Iniciar sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Selecciona una opción (1, 2 o 3): ")

        try:
            if opcion == "1":
                username_input = input("Nombre de usuario: ")
                password_input = maskpass.askpass("Contraseña: ")
                if sistema.login(username_input, password_input):
                    print(f"✅ ¡Acceso concedido para {username_input}!.")
                    mostrar_menu_cuentas(username_input.lower())
                else:
                    print("❌ Usuario o contraseña incorrectos.")

            elif opcion == "2":
                username_input = input("Elige un nombre de usuario: ")
                password1_input = maskpass.askpass("Crea una contraseña: ")
                password2_input = maskpass.askpass("Confirma tu contraseña: ")

                resultado = sistema.register(username_input, password1_input, password2_input)

                if resultado == RegisterResult.USER_EXISTS:
                    print("⚠️ El nombre de usuario ya está en uso.")
                elif resultado == RegisterResult.PASSWORDS_DO_NOT_MATCH:
                    print("⚠️ Las contraseñas no coinciden.")
                elif resultado == RegisterResult.INVALID_PASSWORD:
                    print("❌ Contraseña inválida. Debe tener entre 8 y 12 caracteres, incluir al menos una mayúscula, una minúscula, un número, y no contener espacios.")
                elif resultado == RegisterResult.SUCCESS:
                    print("✅ Registro exitoso. Ya podés iniciar sesión.")

            elif opcion == "3":
                print("Saliendo de la aplicación...")
                sys.exit()
            else:
                print("❌ Opción inválida. Debes ingresar 1, 2 o 3.")
        
        except Exception as e:
            print(e)
