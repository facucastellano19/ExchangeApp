# Aplicación de Gestión de Cuentas y Divisas

Este proyecto es una aplicación de escritorio desarrollada con Python y PyQt6 que permite a los usuarios gestionar sus cuentas, depositar dinero y realizar operaciones de compra/venta de diferentes divisas. Las cotizaciones de las divisas se obtienen en tiempo real a través de una API externa.

## Características

*   **Autenticación de Usuarios:** Registro y login seguro de usuarios con contraseñas hasheadas usando `bcrypt`.
*   **Gestión de Cuentas:** Los usuarios pueden crear y visualizar cuentas en diferentes divisas.
*   **Depósitos:** Posibilidad de depositar fondos en cuentas ARS.
*   **Compra/Venta de Divisas:** Realizar transacciones entre diferentes divisas con cotizaciones actualizadas.
*   **Persistencia de Datos:** Utiliza `SQLObject` con una base de datos MySQL para almacenar información de usuarios y cuentas.
*   **Interfaz Gráfica:** Desarrollada con PyQt6 para una experiencia de usuario intuitiva.

## Estructura del Proyecto

El proyecto está organizado en las siguientes carpetas principales:

*   `Business/`: Contiene la lógica de negocio de la aplicación, incluyendo la gestión de cuentas (`account_manager.py`) y la autenticación de usuarios (`auth.py`).
*   `Data/`: Maneja la serialización y persistencia de datos, interactuando con la base de datos MySQL a través de `SQLObject` (`serializer.py`).
*   `Presentation/`: Contiene la lógica de la interfaz de usuario, como el menú principal (`menu.py`).
*   `screens/`: Almacena los archivos `.ui` (diseños de interfaz de usuario creados con Qt Designer) y sus correspondientes archivos Python generados (`ui_*.py`).
*   `main.py`: Punto de entrada principal de la aplicación.
*   `requirements.txt`: Lista de dependencias del proyecto.
*   `monedas.json`: Archivo para almacenar en caché las monedas válidas obtenidas de la API.

## Requisitos

Para ejecutar esta aplicación, necesitarás tener Python instalado (versión 3.8 o superior recomendada) y una base de datos MySQL configurada.

### Dependencias de Python

Instala las dependencias de Python usando `pip`:

```bash
pip install -r requirements.txt
```

### Configuración de la Base de Datos MySQL

1.  Asegúrate de tener un servidor MySQL en ejecución.
2.  Crea una base de datos llamada `exchangeApp`.
3.  Crea un usuario `guest` con contraseña `1234` (estas son credenciales de ejemplo) y otórgale permisos sobre la base de datos `exchangeApp`.
    (Alternativamente, puedes modificar la cadena de conexión en `Data/serializer.py` para usar tus propias credenciales de base de datos).

    ```sql
    CREATE DATABASE exchangeApp;
    CREATE USER 'guest'@'localhost' IDENTIFIED BY '1234';
    GRANT ALL PRIVILEGES ON exchangeApp.* TO 'guest'@'localhost';
    FLUSH PRIVILEGES;
    ```

## Ejecución de la Aplicación

Una vez que hayas configurado los requisitos, puedes ejecutar la aplicación desde el archivo `main.py`:

```bash
python main.py
```

## Uso de la API de Cotizaciones

La aplicación utiliza la API de CurrencyFreaks para obtener las cotizaciones de las divisas. La clave API está incrustada en el código (`Business/account_manager.py`).
