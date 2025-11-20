# WooCommerce API REST Automation Framework

Un Framework de automatización de pruebas diseñado para validar la funcionalidad de los *endpoints* principales de la API REST de **WooCommerce** utilizando Python y Pytest.

## Introducción

Este proyecto es un **Framework de Automatización de Pruebas** construido en Python, enfocado en el aseguramiento de la calidad (QA) de la **API REST de WooCommerce**. El objetivo principal es la validación de las operaciones **CRUD** (Crear, Leer, Actualizar, Eliminar) para los siguientes módulos:

1.  **Productos (`/products`)**: Gestión de catálogo.
2.  **Clientes (`/customers`)**: Gestión de perfiles de usuario.

El *framework* está diseñado para ejecutarse en un entorno de Integración Continua (CI) y utiliza técnicas de diseño de pruebas (Partición de Equivalencias, Valores Límite, Heurísticas) para cubrir escenarios positivos y negativos.

---

## Requisitos Previos

Para ejecutar el *framework* localmente, se requieren los siguientes componentes:

* **Python:** Versión 3.8 o superior.
* **Git:** Para clonar el repositorio.
* **Instalación de WooCommerce:** Una instancia activa y funcional de WordPress con el plugin **WooCommerce** instalado y configurado.

---

## Configuración e Instalación

Sigue estos pasos ordenados para poner en marcha el *framework* en tu entorno local.

### 1. Clonar el Repositorio

Utiliza el siguiente comando para clonar el proyecto a tu máquina local:

```bash
git clone git@github.com:RodrigoFlo66/woocommerce_api.git
cd woocommerce_api
```
### 2. Configurar el Entorno de WooCommerce

Es necesario que tu instalación de WordPress/WooCommerce cumpla con lo siguiente:

- Permalinks: Asegúrate de que la configuración de Enlaces Permanentes (Settings > Permalinks) NO sea la opción "Simple" (debe ser "Nombre de la entrada" o similar) para que la API REST funcione correctamente.

- Credenciales API: Genera las credenciales de API REST en WooCommerce (Ajustes > Avanzado > REST API). Necesitarás pares de claves con diferentes permisos para cubrir todos los escenarios de prueba:

    - Credenciales con permisos de Lectura/Escritura.
    - Credenciales con permisos de Solo Lectura.
    - Credenciales con permisos de Solo Escritura.
    - Un secreto de API Expirado.
        
### 3. Crear y Configurar Variables de Entorno

El framework utiliza un archivo .env para gestionar las credenciales de forma segura.

- Crea un archivo llamado .env en la raíz del proyecto.

- Copia las siguientes variables y sustituye los valores con tus credenciales reales generadas en el paso anterior.

```bash
# URL base de tu instalación de WordPress/WooCommerce
BASE_URL=http://tu-dominio-o-localhost

# Credenciales con permisos de Lectura/Escritura (Administrador)
API_KEY=tu_key_admin_aqui
API_SECRET=tu_secret_admin_aqui

# Credenciales con permisos de Solo Lectura
API_KEY_READ=tu_key_read_aqui
API_SECRET_READ=tu_secret_read_aqui

# Credenciales con permisos de Solo Escritura
API_KEY_WRITE=tu_key_write_aqui
API_SECRET_WRITE=tu_secret_write_aqui

# Un secreto deliberadamente expirado (para pruebas negativas de seguridad)
API_SECRET_EXPIRED=un_secreto_expirado_o_aqui
```
### 4. Instalar Dependencias de Python

Instala todas las librerías necesarias (Pytest, requests, python-dotenv, Faker, etc.) desde el archivo requirements.txt:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Ejecución de Pruebas

El framework está configurado para ser ejecutado mediante Pytest. Puedes ejecutar conjuntos completos, módulos específicos o tests marcados.

Ejecución Completa

Para ejecutar todos los tests de todos los módulos:
```bash
pytest
```
Ejecución por Módulos

Ejecuta todos los tests dentro de un módulo específico (Productos o Clientes):
```bash
# Ejecutar solo tests del módulo Clientes
pytest tests/customers

# Ejecutar solo tests del módulo Productos
pytest tests/products
```
Ejecución por Marcadores (Marks)

Los tests están clasificados con marcadores (marks) para permitir la ejecución de subconjuntos específicos (ej., pruebas positivas, pruebas negativas, o smoke tests):
```bash
# Ejecutar solo las pruebas de humo (Smoke Tests)
pytest -m "smoke"

# Ejecutar solo las pruebas positivas (escenarios de éxito)
pytest -m "positive"

# Ejecutar solo las pruebas negativas (escenarios de error, seguridad, validación)
pytest -m "negative"
```

## Generación de Reportes

Para generar el reporte detallado con Allure Reports, ejecuta Pytest con el flag --alluredir y luego levanta el servidor de reportes:

```bash
# 1. Ejecutar tests y generar archivos de resultados
pytest --alluredir=./allure-results

# 2. Servir el reporte en tu navegador (requiere tener Allure CLI instalado)
allure serve allure-results
```
