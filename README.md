# 🔥 Anton Enhanced - Sistema Autónomo de Pentesting

![Version](https://img.shields.io/badge/version-4.1-red.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)

## 🎯 Descripción

**Anton Enhanced** es un sistema de pentesting completamente autónomo basado en IA que utiliza el modelo **Hermes-3-Llama-3.1-8B** para ejecutar operaciones de seguridad avanzadas con máxima independencia y capacidad de auto-aprendizaje.

### ✨ Características Principales

- 🧠 **Auto-aprendizaje continuo** - Mejora automáticamente con cada operación
- 🔥 **Temperatura 1.5** - Máxima creatividad e independencia operacional
- 🤖 **Autonomía total** - Zero confirmaciones, ejecución directa de comandos
- 📊 **Resultados en tiempo real** - Todo se muestra en pantalla, sin archivos
- 🛠️ **Auto-instalación** - Instala automáticamente herramientas faltantes
- 🔄 **Mejora continua** - Se perfecciona con cada operación ejecutada
- 📱 **Interfaz Telegram** - Control completo desde Telegram
- 🎯 **Operaciones distribuidas** - Coordinación de múltiples nodos

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Telegram Bot   │◄──►│   Flask API     │◄──►│  LLM Server     │
│  (Interface)    │    │  (Anton Core)   │    │  (Hermes-3)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ User Commands   │    │ Operation Log   │    │ Knowledge Base  │
│ & Notifications │    │ & Results       │    │ & Learning      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🚀 Instalación Rápida

### Prerrequisitos

- Ubuntu/Debian Linux
- Python 3.8+
- 8GB+ RAM recomendado
- Privilegios sudo
- Modelo Hermes-3-Llama-3.1-8B.Q5_K_M.gguf

### Instalación Automática

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/anton-enhanced.git
cd anton-enhanced

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install flask flask-cors requests telebot

# Configurar permisos
chmod +x start_anton.sh

# Iniciar Anton
./start_anton.sh
```

## ⚙️ Configuración

### 1. Modelo LLM

Descargar el modelo Hermes-3:
```bash
mkdir -p models
cd models
wget https://huggingface.co/NousResearch/Hermes-3-Llama-3.1-8B-GGUF/resolve/main/Hermes-3-Llama-3.1-8B.Q5_K_M.gguf
```

### 2. Telegram Bot (Opcional)

1. Crear bot con @BotFather en Telegram
2. Editar `telegram_bot.py`:
```python
TOKEN = "TU_TOKEN_AQUI"
AUTHORIZED_USER_ID = TU_USER_ID
```

### 3. Configuración Avanzada

Editar `anton_config.json`:
```json
{
  "operation_settings": {
    "max_timeout": 1800,
    "auto_escalate": true,
    "learning_mode": true
  },
  "paths": {
    "log_dir": "/var/log/anton",
    "results_dir": "/home/user/results"
  }
}
```

## 🎮 Uso Básico

### Comandos Principales

```bash
# Iniciar sistema
./start_anton.sh

# Verificar estado
./start_anton.sh status

# Verificar salud
./start_anton.sh health

# Reiniciar
./start_anton.sh restart

# Detener
./start_anton.sh stop
```

### Ejemplos de Operaciones

#### Via Telegram:
- `192.168.1.100` → Operación autónoma completa
- `example.com` → Reconocimiento + testing web
- `nmap -sS 192.168.1.0/24` → Ejecución directa
- `instala nuclei` → Auto-instalación
- `evalúa wireless` → Assessment WiFi

#### Via API:
```bash
curl -X POST http://localhost:5000/anton \
  -H "Content-Type: application/json" \
  -d '{"prompt": "evalúa 192.168.1.100", "user_id": "admin"}'
```

## 🛠️ Herramientas Soportadas

### Reconocimiento
- `nmap` - Escaneo de red y puertos
- `masscan` - Escaneo rápido masivo
- `subfinder` - Enumeración de subdominios
- `nuclei` - Escaneo de vulnerabilidades
- `amass` - Reconocimiento de activos

### Testing Web
- `nikto` - Escaneo de vulnerabilidades web
- `gobuster` - Enumeración de directorios
- `sqlmap` - Testing de inyección SQL
- `wpscan` - Análisis de WordPress
- `whatweb` - Identificación de tecnologías

### Credenciales
- `hydra` - Ataques de fuerza bruta
- `john` - Cracking de passwords
- `hashcat` - Cracking con GPU
- `medusa` - Fuerza bruta paralela

### Wireless
- `aircrack-ng` - Suite completa WiFi
- `reaver` - Ataques WPS
- `wifite` - Framework automatizado

## 📊 Monitoreo y Logs

### Estados del Sistema

```bash
# Estado general
curl http://localhost:5000/status

# Operaciones activas
curl http://localhost:5000/evaluations

# Logs en tiempo real
tail -f ~/anton_enhanced.log
```

### Métricas de Aprendizaje

Anton mantiene estadísticas de:
- Targets analizados
- Técnicas exitosas por target
- Tasa de éxito por herramienta
- Tiempo promedio de operaciones

## 🔧 API Reference

### Endpoints Principales

| Endpoint | Método | Descripción |
|----------|---------|-------------|
| `/anton` | POST | Ejecutar operación |
| `/status` | GET | Estado del sistema |
| `/evaluations` | GET | Operaciones activas |

### Estructura de Request

```json
{
  "prompt": "192.168.1.100",
  "user_id": "admin",
  "operation_params": {
    "depth": "comprehensive",
    "timeout": 1800
  }
}
```

### Estructura de Response

```json
{
  "response": "🎯 OPERACIÓN AUTÓNOMA INICIADA...",
  "operation_id": "auto_192.168.1.100_1640995200",
  "status": "running"
}
```

## 🧠 Sistema de Auto-Aprendizaje

Anton aprende automáticamente de cada operación:

### Métricas Tracked
- **Técnicas exitosas** por target
- **Tiempo de ejecución** promedio
- **Tasa de éxito** por herramienta
- **Patrones de vulnerabilidades**

### Mejora Automática
- Adapta estrategias basado en historial
- Optimiza secuencias de comandos
- Prioriza técnicas más efectivas
- Reduce falsos positivos

## ⚠️ Consideraciones de Seguridad

### Uso Responsable

> **IMPORTANTE**: Anton está diseñado para pentesting autorizado en entornos controlados.

- ✅ Usar solo en redes propias o autorizadas
- ✅ Obtener permisos explícitos antes de testing
- ✅ Documentar todas las actividades
- ✅ Seguir marcos legales locales

### Configuración Segura

```bash
# Restringir acceso a APIs
iptables -A INPUT -p tcp --dport 5000 -s 127.0.0.1 -j ACCEPT
iptables -A INPUT -p tcp --dport 5000 -j DROP

# Configurar logs seguros
chmod 640 /var/log/anton/*.log
```

## 🐛 Troubleshooting

### Problemas Comunes

#### Error: "llama-server no responde"
```bash
# Verificar proceso
ps aux | grep llama-server

# Revisar logs
tail -f ~/anton_enhanced.log

# Reiniciar
./start_anton.sh restart
```

#### Error: "API no responde"
```bash
# Verificar sintaxis Python
python3 -m py_compile app.py

# Verificar dependencias
pip install -r requirements.txt

# Revisar logs Flask
tail -f ~/anton_flask.log
```

#### Error: "Herramientas faltantes"
```bash
# Auto-instalación
curl -X POST http://localhost:5000/anton \
  -H "Content-Type: application/json" \
  -d '{"prompt": "instala herramientas", "user_id": "admin"}'
```

### Logs de Diagnóstico

```bash
# Logs del sistema
journalctl -u anton-enhanced

# Logs de operaciones
tail -f /var/log/anton/anton_*.log

# Métricas de rendimiento
htop
iotop
```

## 📈 Roadmap

### v4.2 (Próximo)
- [ ] Interfaz web gráfica
- [ ] Integración con Metasploit
- [ ] Reportes automáticos en PDF
- [ ] API de webhooks

### v5.0 (Futuro)
- [ ] Clustering multi-nodo
- [ ] Machine learning avanzado
- [ ] Integración con SIEM
- [ ] Modo stealth avanzado

## 🤝 Contribuir

### Desarrollo

```bash
# Fork del repositorio
git clone https://github.com/tu-usuario/anton-enhanced.git

# Crear rama de feature
git checkout -b feature/nueva-caracteristica

# Commit y push
git commit -m "feat: nueva característica"
git push origin feature/nueva-caracteristica

# Crear Pull Request
```

### Estructura del Código

```
anton-enhanced/
├── app.py              # Core API de Anton
├── telegram_bot.py     # Interfaz Telegram
├── start_anton.sh      # Script de inicio
├── anton_lavey.py      # Coordinador distribuido
├── anton_pentest.py    # Motor de operaciones
├── models/             # Modelos LLM
├── logs/               # Logs del sistema
└── docs/               # Documentación
```

### Guidelines

- **Código limpio** y comentado
- **Tests unitarios** para nuevas features
- **Documentación** actualizada
- **Commits semánticos** (feat, fix, docs, etc.)

## 📄 Licencia

Este proyecto está licenciado bajo la MIT License - ver [LICENSE](LICENSE) para detalles.

## ⚖️ Disclaimer

Este software es para fines **educativos y de testing autorizado únicamente**. Los usuarios son responsables de cumplir con todas las leyes y regulaciones locales. Los desarrolladores no se hacen responsables del mal uso de esta herramienta.

## 📞 Soporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/tu-usuario/anton-enhanced/issues)
- 💬 **Discusiones**: [GitHub Discussions](https://github.com/tu-usuario/anton-enhanced/discussions)
- 📧 **Email**: anton-support@ejemplo.com

---

<div align="center">

**🔥 Anton Enhanced - Pentesting Autónomo con IA 🔥**

*Desarrollado con ❤️ para la comunidad de ciberseguridad*

[⭐ Star](https://github.com/tu-usuario/anton-enhanced) | [🐛 Report Bug](https://github.com/tu-usuario/anton-enhanced/issues) | [💡 Request Feature](https://github.com/tu-usuario/anton-enhanced/issues)

</div>
