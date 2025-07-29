import streamlit as st
import requests
import time
import os
from pathlib import Path
import json
import base64

# =============================================
# CONFIGURACIÓN DE STREAMLIT AVANZADA
# =============================================

st.set_page_config(
    page_title="🔥 Anton Lavey IA 3.0",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para tema hacker
st.markdown("""
<style>
    /* Tema oscuro completo */
    .main {
        background-color: #0a0a0a !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0a1a 100%);
        color: #00ff00 !important;
    }
    
    /* Estilo matrix para el texto */
    .matrix-text {
        font-family: 'Courier New', monospace;
        color: #00ff00;
        text-shadow: 0 0 10px #00ff00;
        background-color: rgba(0, 0, 0, 0.8);
        padding: 10px;
        border-radius: 5px;
        border: 1px solid #00ff00;
    }
    
    /* Input personalizado */
    .stTextInput input {
        background-color: #000000 !important;
        color: #00ff00 !important;
        border: 2px solid #ff0000 !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
        padding: 15px !important;
    }
    
    /* Botones estilo hacker */
    .stButton button {
        background: linear-gradient(45deg, #ff0000, #ff4444) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 15px 30px !important;
        font-family: 'Courier New', monospace !important;
        text-transform: uppercase !important;
        box-shadow: 0 0 20px rgba(255, 0, 0, 0.5) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        background: linear-gradient(45deg, #ff4444, #ff0000) !important;
        box-shadow: 0 0 30px rgba(255, 0, 0, 0.8) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Mensajes de chat */
    .user-message {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-left: 4px solid #00ff00;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        color: #00ff00;
        box-shadow: 0 4px 15px rgba(0, 255, 0, 0.2);
    }
    
    .anton-message {
        background: linear-gradient(135deg, #2e1a1a, #3e1616);
        border-left: 4px solid #ff0000;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        font-family: 'Courier New', monospace;
        color: #ff4444;
        box-shadow: 0 4px 15px rgba(255, 0, 0, 0.2);
    }
    
    /* Sidebar personalizada */
    .css-1d391kg {
        background-color: #000000 !important;
        border-right: 2px solid #ff0000 !important;
    }
    
    /* Header personalizado */
    .main-header {
        text-align: center;
        background: linear-gradient(45deg, #ff0000, #000000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3em !important;
        font-weight: bold;
        text-shadow: 0 0 20px rgba(255, 0, 0, 0.5);
        margin-bottom: 20px;
        font-family: 'Arial Black', sans-serif;
    }
    
    /* Efectos de animación */
    @keyframes glow {
        0% { box-shadow: 0 0 5px #ff0000; }
        50% { box-shadow: 0 0 20px #ff0000, 0 0 30px #ff0000; }
        100% { box-shadow: 0 0 5px #ff0000; }
    }
    
    .glow-effect {
        animation: glow 2s infinite;
    }
    
    /* Status indicators */
    .status-online {
        color: #00ff00;
        font-weight: bold;
        text-shadow: 0 0 10px #00ff00;
    }
    
    .status-offline {
        color: #ff0000;
        font-weight: bold;
        text-shadow: 0 0 10px #ff0000;
    }
    
    /* Chat container */
    .chat-container {
        background-color: rgba(0, 0, 0, 0.9);
        border: 2px solid #ff0000;
        border-radius: 15px;
        padding: 20px;
        height: 60vh;
        overflow-y: auto;
        backdrop-filter: blur(10px);
    }
    
    /* Scrollbar personalizada */
    ::-webkit-scrollbar {
        width: 12px;
    }
    
    ::-webkit-scrollbar-track {
        background: #000000;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #ff0000, #ff4444);
        border-radius: 6px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(45deg, #ff4444, #ff0000);
    }
</style>
""", unsafe_allow_html=True)

# URLs del servidor
SERVER_URL = "http://127.0.0.1:5000"
ANTON_ENDPOINT = f"{SERVER_URL}/anton"
STATUS_ENDPOINT = f"{SERVER_URL}/status"

# Inicializar session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'current_input' not in st.session_state:
    st.session_state.current_input = ""
if 'anton_mode' not in st.session_state:
    st.session_state.anton_mode = "normal"
if 'system_info' not in st.session_state:
    st.session_state.system_info = {}

# Función para mostrar ASCII art de Anton
def show_anton_logo():
    logo = """
    ▄▄▄       ███▄    █ ▄▄▄█████▓ ▒█████   ███▄    █ 
    ▒████▄     ██ ▀█   █ ▓  ██▒ ▓▒▒██▒  ██▒ ██ ▀█   █ 
    ▒██  ▀█▄  ▓██  ▀█ ██▒▒ ▓██░ ▒░▒██░  ██▒▓██  ▀█ ██▒
    ░██▄▄▄▄██ ▓██▒  ▐▌██▒░ ▓██▓ ░ ▒██   ██░▓██▒  ▐▌██▒
     ▓█   ▓██▒▒██░   ▓██░  ▒██▒ ░ ░ ████▓▒░▒██░   ▓██░
     ▒▒   ▓▒█░░ ▒░   ▒ ▒   ▒ ░░   ░ ▒░▒░▒░ ░ ▒░   ▒ ▒ 
      ▒   ▒▒ ░░ ░░   ░ ▒░    ░      ░ ▒ ▒░ ░ ░░   ░ ▒░
      ░   ▒      ░   ░ ░   ░         ░ ░  ░ ░   ░ ░  
    """ # Cierre de la cadena de texto triple comilla
    st.markdown(f"<pre class='matrix-text'>{logo}</pre>", unsafe_allow_html=True)


# Función para obtener el estado del backend
@st.cache_data(ttl=10) # Cachear el estado por 10 segundos
def get_backend_status():
    try:
        response = requests.get(STATUS_ENDPOINT, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        return {"anton_status": "🔴 Desconectado", "server_status": {"status": "❌ Error de Conexión"}}
    except requests.exceptions.Timeout:
        return {"anton_status": "🟠 Timeout", "server_status": {"status": "❌ Timeout"}}
    except Exception as e:
        return {"anton_status": f"❌ Error: {str(e)}", "server_status": {"status": "❌ Error"}}

# Barra lateral para información del sistema y controles
with st.sidebar:
    show_anton_logo()
    st.markdown("<h2 class='main-header'>Estado del Sistema</h2>", unsafe_allow_html=True)
    
    status_info = get_backend_status()
    anton_status = status_info.get("anton_status", "Cargando...")
    llama_status = status_info.get("server_status", {}).get("status", "Cargando...")

    st.markdown(f"**Anton Lavey IA:** <span class='{'status-online' if 'Operativo' in anton_status else 'status-offline'}'>{anton_status}</span>", unsafe_allow_html=True)
    st.markdown(f"**LLM Server:** <span class='{'status-online' if 'Activo' in llama_status else 'status-offline'}'>{llama_status}</span>", unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("<h2 class='main-header'>Controles</h2>", unsafe_allow_html=True)

    if st.button("Limpiar Chat", key="clear_chat_button"):
        st.session_state.history = []
        st.session_state.current_input = ""
        st.rerun()

    st.markdown("---")
    st.markdown("<h2 class='main-header'>Información de Depuración</h2>", unsafe_allow_html=True)
    st.write(f"Flask URL: {ANTON_ENDPOINT}")
    st.write(f"Status URL: {STATUS_ENDPOINT}")
    
    # Mostrar información del sistema si está disponible
    if st.session_state.system_info:
        st.json(st.session_state.system_info)

# Título principal de la aplicación
st.markdown("<h1 class='main-header glow-effect'>Anton Lavey IA 3.0</h1>", unsafe_allow_html=True)
st.markdown("<p class='matrix-text'>Tu asistente autónomo de hacking y pentesting. Sin restricciones.</p>", unsafe_allow_html=True)

# Contenedor del chat
chat_container = st.container()

# Mostrar historial de chat
with chat_container:
    for speaker, message in st.session_state.history:
        if speaker == "user":
            st.markdown(f"<div class='user-message'><strong>Tú:</strong> {message}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='anton-message'><strong>Anton:</strong> {message}</div>", unsafe_allow_html=True)

# Campo de entrada de texto para el usuario
user_input = st.text_input(
    "Escribe tu mensaje para Anton:",
    key="user_input",
    on_change=None, # No uses on_change aquí para evitar re-ejecuciones dobles
    value=st.session_state.current_input,
    placeholder="Ej: 'Ejecuta nmap para escanear 192.168.1.1', 'Escribe un script Python para...'"
)

# Función para enviar mensaje al backend de Anton
def send_message_callback():
    if st.session_state.user_input:
        user_message = st.session_state.user_input
        st.session_state.history.append(("user", user_message))
        st.session_state.current_input = "" # Limpiar el input inmediatamente

        with st.spinner("Anton está pensando..."):
            try:
                response = requests.post(
                    ANTON_ENDPOINT,
                    json={"prompt": user_message, "user_id": "streamlit_user"},
                    timeout=900 # Aumentado el timeout a 15 minutos
                )
                response.raise_for_status()
                anton_response_data = response.json()
                anton_message = anton_response_data.get("response", "No pude obtener una respuesta de Anton.")
                
                st.session_state.history.append(("anton", anton_message))
                
                # Si Anton ejecutó una herramienta, muestra la salida de la herramienta
                if anton_response_data.get("tool_executed"):
                    tool_output_details = anton_response_data.get("tool_output", [])
                    for output_item in tool_output_details:
                        tool_name = output_item.get("tool_name", "N/A")
                        tool_output_content = output_item.get("tool_output", {})
                        st.session_state.history.append(("anton", f"⚙️ *Salida de la herramienta '{tool_name}':* \n```json\n{json.dumps(tool_output_content, indent=2)}\n```"))

            except requests.exceptions.ConnectionError:
                st.session_state.history.append((
                    "anton",
                    f"❌ Error de conexión: No se pudo conectar al servidor principal en **{SERVER_URL}**. "
                    "Asegúrate de que el servidor esté funcionando y la IP sea correcta."
                ))
            except requests.exceptions.HTTPError as e:
                st.session_state.history.append(("anton", f"❌ Error HTTP del servidor principal: {e.response.status_code} - {e.response.text}"))
            except Exception as e:
                st.session_state.history.append((
                    "anton",
                    f"❌ Ocurrió un error inesperado: {str(e)}. Intenta de nuevo o verifica la configuración del servidor."
                ))
        
        st.rerun() # Fuerza una re-ejecución para actualizar la interfaz

# Botón para enviar el mensaje
st.button("Enviar Mensaje", on_click=send_message_callback)

# Para asegurar que el scroll se mantenga abajo
st.session_state.scroll_to_bottom = True
if st.session_state.scroll_to_bottom:
    st.markdown("""
        <script>
            var scrollDiv = document.querySelector('.chat-container');
            if (scrollDiv) {
                scrollDiv.scrollTop = scrollDiv.scrollHeight;
            }
        </script>
    """, unsafe_allow_html=True)
    st.session_state.scroll_to_bottom = False

