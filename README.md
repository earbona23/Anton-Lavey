# Anton Lavey IA 3.0 - Framework Autónomo de Pentesting

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-API-green?style=for-the-badge&logo=flask)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?style=for-the-badge&logo=streamlit)
![Linux](https://img.shields.io/badge/Linux-Sudo_Powered-lightgrey?style=for-the-badge&logo=linux)

```
██████╗  ██████╗ ██╗    ██╗███████╗██████╗ 
██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██║ █╗ ██║█████╗  ██████╔╝
██╔═══╝ ██║   ██║██║███╗██║██╔══╝  ██╔══██╗
██║     ╚██████╔╝╚███╔███╔╝███████╗██║  ██║
╚═╝      ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝
```

**Anton Lavey IA 3.0** es un framework experimental para un agente de IA autónomo, diseñado para realizar tareas de pentesting y administración de sistemas en **entornos de laboratorio controlados**. Utiliza un modelo de lenguaje local (LLM) para razonar y tomar decisiones, y un conjunto de herramientas seguras para interactuar con el sistema operativo anfitrión.

El sistema está construido con una filosofía de **poder controlado**: aunque el núcleo de IA es muy libre, está encapsulado en un framework (`anton_pentest.py`) que impone políticas de seguridad estrictas, como la validación de objetivos y el registro de auditoría.

---

## 🏛️ Arquitectura del Sistema

Anton opera con una arquitectura modular que separa la inteligencia, la lógica y las interfaces.

```
+---------------------------------+
|        Interfaces de Usuario    |
| (Streamlit, Telegram, WhatsApp) |
+----------------+----------------+
                 |
                 v
+----------------+----------------+
|     API Server (app.py)         |
| (Flask - El Cerebro de Anton)   |
+----------------+----------------+
                 |
+----------------v----------------+      +----------------+----------------+
|  Lógica y Herramientas          |------>|      LLM (llama-server)       |
| (anton_pentest.py, Scripts Bash)|      | (Nous Hermes Llama2 13B)      |
+----------------+----------------+      +----------------+----------------+
                 |
                 v
+----------------+----------------+
| Sistema Operativo Anfitrión     |
| (Comandos con privilegios sudo) |
+---------------------------------+
```

---

## ✨ Características Principales

* **Núcleo de IA Local:** Utiliza el modelo `nous-hermes-llama2-13b` a través de `llama.cpp` para un funcionamiento offline y privado.
* **Control Total del Sistema:** Opera como un usuario con privilegios `sudo` sin contraseña, permitiéndole instalar herramientas, gestionar servicios y modificar el sistema.
* **Framework de Pentesting Seguro:** A pesar de sus privilegios, todas las operaciones de pentesting son manejadas por `anton_pentest.py`, que incluye:
    * Validación de objetivos contra una lista blanca.
    * Prohibición explícita de atacar objetivos públicos.
    * Requerimiento de autorización para tareas delicadas.
    * Auditoría completa de todas las acciones.
* **Múltiples Interfaces:** Accesible a través de un front-end web (Streamlit) y un bot de Telegram.
* **Sincronización con GitHub:** Capacidad de hacer backup y sincronizar sus archivos de configuración y scripts importantes a un repositorio Git.
* **Arranque Unificado:** Un único script (`start_anton.sh`) se encarga de la configuración del sistema, instalación de dependencias y el lanzamiento de todos los servicios.

---

## 警告 Advertencia de Seguridad

Este software está diseñado **exclusivamente para fines educativos y para ser utilizado en entornos de laboratorio aislados y autorizados.**

* **NO EXPONER A INTERNET:** El agente tiene privilegios de `sudo`. Exponerlo directamente a internet sin medidas de seguridad extremas es increíblemente peligroso y podría resultar en el compromiso total de la máquina anfitriona.
* **USO BAJO TU PROPIO RIESGO:** El autor no se hace responsable del mal uso de esta herramienta. Eres el único responsable de tus acciones.

---

## 🚀 Instalación y Arranque

El sistema está diseñado para ser configurado con un solo comando en un sistema basado en Ubuntu/Debian.

### Prerrequisitos
1.  Un sistema operativo Linux (Ubuntu 22.04+ recomendado).
2.  Python 3.10 o superior.
3.  `git` y `python3-venv` instalados (`sudo apt install git python3-venv`).
4.  **Modelo de Lenguaje:** Descargar el modelo `nous-hermes-llama2-13b.Q5_K_M.gguf` y colocarlo en un directorio llamado `models`.
5.  **Llama.cpp:** Clonar y compilar `llama.cpp` en el directorio raíz del proyecto. El script de inicio buscará el ejecutable `llama-server` dentro de esta carpeta.

### Configuración de Credenciales
Antes del primer arranque, es necesario configurar las credenciales:
1.  **Telegram:** Crea un archivo `telegram_bot.py` o integra tu token directamente en `app.py` o `start_anton.sh` si lo deseas.
2.  **GitHub Sync:** Edita el archivo `github_sync.sh` y añade tu usuario, email y un **Token de Acceso Personal** de GitHub con permisos de `repo`.

### Arranque
Una vez cumplidos los prerrequisitos, el arranque es tan simple como ejecutar un solo script.

```bash
# Dar permisos de ejecución al script
chmod +x start_anton.sh

# Ejecutar el script maestro
./start_anton.sh
```

Este comando se encargará de:
1.  Verificar y configurar los permisos `sudo`.
2.  Instalar todas las herramientas de pentesting necesarias (`nmap`, `hydra`, etc.).
3.  Crear el entorno virtual de Python e instalar las dependencias.
4.  Lanzar todos los servicios (LLM, API, Frontend, etc.) en el orden correcto.

---

## 🛠️ Uso

Una vez que el sistema esté activo, puedes interactuar con Anton de las siguientes maneras:

* **Frontend Web:** Abre tu navegador y ve a `http://127.0.0.1:8501`.
* **Bot de Telegram:** Busca tu bot en Telegram y envíale mensajes.

### Ejemplos de Comandos

* `hola anton como estas` (Para una conversación normal)
* `escanea la red 192.168.1.0/24 con un escaneo básico` (Para usar una herramienta segura)
* `sincroniza el proyecto con github` (Para ejecutar el script de backup)
* `escribe un archivo en notas/plan.txt con el contenido: 'Paso 1: Reconocimiento'` (Para guardar notas)
