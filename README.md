# README – Proyecto VetCare

## 🐾 Descripción del Proyecto

VetCare es una aplicación web desarrollada en **Django** que facilita la gestión de una clínica veterinaria. Permite a los usuarios:

* Registrarse e iniciar sesión.
* Agendar citas veterinarias.
* Ver y administrar citas.
* Consultar productos.
* Realizar compras mediante carrito y checkout.
* Ver historial de compras.

## 📂 Estructura del Proyecto

```
VETCARE/
│
├── crud_app/                # Aplicación principal
│   ├── migrations/          # Migraciones de BD
│   ├── templates/           # Plantillas HTML
│   ├── admin.py             # Configuración del panel Admin
│   ├── apps.py
│   ├── forms.py             # Formularios
│   ├── models.py            # Modelos de BD
│   ├── urls.py              # Rutas internas
│   ├── views.py             # Lógica de vistas
│
├── vetcare/                 # Configuración global del proyecto
│   ├── settings.py          # Ajustes principales
│   ├── urls.py              # Rutas globales
│   ├── wsgi.py / asgi.py    # Archivos de despliegue
│
├── db.sqlite3               # Base de datos
├── venv/                    # Entorno virtual
```

##  Requisitos Previos

* **Python 3.10 o superior**
* **pip** instalado
* **Django 4 o superior**
* Entorno virtual opcional (recomendado)

## 🚀 Instalación y Ejecución

### 1 Crear entorno virtual

```
python -m venv venv
```

###  2 Activar entorno virtual

**Windows:**

```
venv\Scripts\activate
```

**Linux/Mac:**

```
bash venv/bin/activate
```

### 3 Instalar dependencias

```
pip install -r requirements.txt
```

(Si no tienes este archivo, te lo puedo generar.)

### 4 Aplicar migraciones

```
python manage.py migrate
```

### 5 Crear superusuario

```
python manage.py createsuperuser
```

### 6 Ejecutar el servidor

```
python manage.py runserver
```

Acceder en el navegador:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

 Funcionalidades Principales

* Registro e inicio de sesión.
* Agendamiento de citas veterinarias.
* Listado de citas.
* Catálogo de productos.
* Carrito de compras.
* Checkout.
* Historial de compras.


Proyecto desarrollado para fines académicos.

## 📄 Licencia

Uso académico y personal.
