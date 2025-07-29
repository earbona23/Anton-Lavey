#!/bin/bash

# =============================================
# ANTON LAVEY IA 3.0 - SCRIPT MAESTRO UNIFICADO
# =============================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Funciones de impresión
print_status() { echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] $1${NC}"; }
print_warning() { echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"; }
print_error() { echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"; }
print_info() { echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $1${NC}"; }

# Variables de configuración
BASE_DIR="/home/anton-lavey/transformers"
MODELS_DIR="$BASE_DIR/models"
LOGS_DIR="$HOME"
VENV_DIR="$BASE_DIR/venv"
MODEL_NAME="nous-hermes-llama2-13b.Q5_K_M.gguf"
MODEL_PATH="$MODELS_DIR/$MODEL_NAME"
LLAMA_PORT=11435
FLASK_PORT=5000
FRONTEND_PORT=8501
LLAMA_LOG="$LOGS_DIR/llama.log"
FLASK_LOG="$LOGS_DIR/flask.log"
FRONTEND_LOG="$LOGS_DIR/frontend.log"
BOT_LOG="$LOGS_DIR/bot.log"

# Banner de Anton
show_banner() {
    echo -e "${CYAN}"
    cat << "EOF"
██████╗  ██████╗ ██╗    ██╗███████╗██████╗ 
██╔══██╗██╔═══██╗██║    ██║██╔════╝██╔══██╗
██████╔╝██║   ██║██║ █╗ ██║█████╗  ██████╔╝
██╔═══╝ ██║   ██║██║███╗██║██╔══╝  ██╔══██╗
██║     ╚██████╔╝╚███╔███╔╝███████╗██║  ██║
╚═╝      ╚═════╝  ╚══╝╚══╝ ╚══════╝╚═╝  ╚═╝

█████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ██╗
██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗  ██║
███████║██╔██╗ ██║   ██║   ██║   ██║██╔██╗ ██║
██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╗██║
██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝
EOF
    echo -e "${NC}"
    echo -e "${PURPLE}🔥 SUPER ADMIN IA 3.0 - CONFIGURACIÓN COMPLETA 🔥${NC}"
    echo ""
}

# =============================================
# FASE 1: CONFIGURACIÓN DE SUDO Y HERRAMIENTAS
# =============================================

setup_system() {
    print_info "Configurando privilegios de super administrador..."
    if ! sudo -n true 2>/dev/null; then
        print_warning "Configurando privilegios sudo sin contraseña..."
        (echo "anton-lavey ALL=(ALL) NOPASSWD: ALL" | sudo tee /etc/sudoers.d/anton-lavey > /dev/null)
        sudo usermod -aG sudo anton-lavey 2>/dev/null || true
    fi
    print_status "Privilegios sudo verificados ✅"

    print_info "Instalando/Verificando herramientas de pentesting..."
    sudo apt-get update -y > /dev/null 2>&1
    
    local tools=(
        "nmap" "tcpdump" "masscan" "gobuster" "nikto" "sqlmap" 
        "hydra" "john" "hashcat" "curl" "wget" "netcat-openbsd" "tshark"
    )
    
    for tool in "${tools[@]}"; do
        if ! command -v "$tool" > /dev/null 2>&1; then
            print_info "📦 Instalando $tool..."
            sudo apt-get install -y "$tool" > /dev/null 2>&1 || print_warning "⚠️  No se pudo instalar $tool"
        fi
    done
    print_status "Herramientas de pentesting verificadas ✅"
}

# =============================================
# FASE 2: PREPARACIÓN DEL ENTORNO
# =============================================

check_dependencies() {
    print_info "Verificando dependencias del sistema..."
    if [ ! -f "$MODEL_PATH" ]; then
        print_error "Modelo no encontrado: $MODEL_PATH"; exit 1;
    fi
    mkdir -p "$LOGS_DIR"
    
    if [ ! -d "$VENV_DIR" ]; then
        print_warning "Creando nuevo entorno virtual..."
        python3 -m venv "$VENV_DIR"
        source "$VENV_DIR/bin/activate"
        pip install --upgrade pip > /dev/null 2>&1
        # Se asume que app.py importará y usará anton_pentest.py
        pip install flask flask-cors requests streamlit pyTelegramBotAPI ipaddress > /dev/null 2>&1
    fi
    print_status "Dependencias verificadas ✅"
}

kill_existing_processes() {
    print_info "Eliminando procesos existentes..."
    for port in $LLAMA_PORT $FLASK_PORT $FRONTEND_PORT; do
        sudo lsof -ti:$port | xargs -r sudo kill -9 2>/dev/null || true
    done
    pkill -f "llama-server|app.py|telegram_bot.py|frontend.py" 2>/dev/null || true
    sleep 3
    print_status "Procesos existentes eliminados ✅"
}

setup_environment() {
    print_info "Configurando entorno de ejecución..."
    cd "$BASE_DIR"
    if [ -f "/opt/intel/oneapi/setvars.sh" ]; then
        print_info "Cargando entorno Intel oneAPI..."
        source /opt/intel/oneapi/setvars.sh --force > /dev/null 2>&1
    fi
    source "$VENV_DIR/bin/activate"
    print_status "Entorno configurado ✅"
}

# =============================================
# FASE 3: INICIO DE SERVICIOS
# =============================================

start_llama_server() {
    print_info "Iniciando llama-server optimizado..."
    local LLAMA_SERVER_BIN=$(find "$BASE_DIR/llama.cpp" -name "llama-server" -type f -executable | head -1)
    if [ -z "$LLAMA_SERVER_BIN" ]; then print_error "No se encontró llama-server."; return 1; fi
    
    local args=(-m "$MODEL_PATH" --host "0.0.0.0" --port $LLAMA_PORT -t 8 -c 4096 --mlock --jinja --log-disable)
    nohup "$LLAMA_SERVER_BIN" "${args[@]}" > "$LLAMA_LOG" 2>&1 &
    local LLAMA_PID=$!
    print_info "llama-server iniciado con PID: $LLAMA_PID. Esperando 60s para estabilización..."
    sleep 60
    
    if ! ps -p $LLAMA_PID > /dev/null; then
        print_error "llama-server falló al iniciar. Ver log: $LLAMA_LOG"; tail -n 20 "$LLAMA_LOG"; return 1;
    fi
    print_status "llama-server activo y estable ✅"
}

start_flask_server() {
    print_info "Iniciando servidor Flask (API)..."
    # Se asume que app.py ahora importa y utiliza anton_pentest.py
    nohup python3 app.py > "$FLASK_LOG" 2>&1 &
    print_info "Flask server iniciado con PID: $!. Esperando 10s..."
    sleep 10
    
    if ! curl -s http://127.0.0.1:$FLASK_PORT/status > /dev/null 2>&1; then
        print_error "Flask server no responde. Ver log: $FLASK_LOG"; tail -n 20 "$FLASK_LOG"; return 1;
    fi
    print_status "Servidor Flask activo ✅"
}

start_telegram_bot() {
    print_info "Iniciando bot de Telegram..."
    nohup python3 telegram_bot.py > "$BOT_LOG" 2>&1 &
    print_status "Bot de Telegram activo con PID: $! ✅"
}

start_frontend() {
    print_info "Iniciando frontend Streamlit..."
    nohup streamlit run frontend.py --server.port $FRONTEND_PORT --server.address 0.0.0.0 --server.headless true > "$FRONTEND_LOG" 2>&1 &
    print_status "Frontend Streamlit activo con PID: $! ✅"
}

# =============================================
# FASE 4: VERIFICACIÓN DEL SISTEMA
# =============================================

show_system_status() {
    echo ""
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}                🔥 ANTON LAVEY IA 3.0 - SUPER ADMIN ACTIVO 🔥             ${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}📊 SERVICIOS PRINCIPALES:${NC}"
    echo -e "   🧠 LLM Server (llama.cpp):    http://127.0.0.1:$LLAMA_PORT"
    echo -e "   🌐 API Server (Flask):        http://127.0.0.1:$FLASK_PORT"
    echo -e "   🖥️ Frontend (Streamlit):      http://127.0.0.1:$FRONTEND_PORT"
    echo -e "   📞 Bot de Telegram:           Activo"
    echo ""
    echo -e "${GREEN}🛠️ CAPACIDADES DISPONIBLES:${NC}"
    echo -e "   🔐 Privilegios sudo:          ✅ Sin contraseña"
    local tools_ok=0
    for tool in nmap sqlmap hydra; do if command -v $tool >/dev/null 2>&1; then ((tools_ok++)); fi; done
    echo -e "   🔍 Herramientas Pentesting:   ✅ $tools_ok herramientas clave instaladas"
    echo ""
    echo -e "${GREEN}📋 ARCHIVOS DE LOG:${NC}"
    echo -e "   Para monitorear: ${YELLOW}tail -f $LOGS_DIR/{flask.log,bot.log}${NC}"
    echo ""
    echo -e "${GREEN}✅ Sistema completamente operativo con privilegios totales${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
}

# =============================================
# FUNCIÓN PRINCIPAL
# =============================================

main() {
    show_banner
    
    print_info "🚀 Iniciando configuración completa de Anton Lavey IA 3.0..."
    
    print_info "📋 FASE 1: Configuración del sistema"
    setup_system
    
    print_info "📋 FASE 2: Preparación del entorno"
    check_dependencies
    kill_existing_processes
    setup_environment
    
    print_info "📋 FASE 3: Inicio de servicios"
    start_llama_server || { print_error "Fallo crítico en llama-server. Abortando."; exit 1; }
    start_flask_server || { print_error "Fallo crítico en Flask server. Abortando."; exit 1; }
    start_telegram_bot
    start_frontend
    
    print_info "📋 FASE 4: Verificación del sistema"  
    sleep 5
    show_system_status
    
    print_info "🎉 Anton Lavey IA 3.0 está completamente listo y operativo!"
    print_warning "💡 La primera consulta puede ser lenta. Después será muy rápido."
}

# Manejo de limpieza al cerrar
cleanup() {
    print_warning "\nRecibida señal de interrupción. Limpiando procesos..."
    kill_existing_processes
    exit 0
}
trap cleanup SIGINT SIGTERM

# Verificar que se ejecuta como el usuario correcto
if [ "$USER" != "anton-lavey" ]; then
    print_error "Este script debe ejecutarse como el usuario 'anton-lavey'"
    exit 1
fi

# Ejecutar función principal
main "$@"
