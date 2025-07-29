#!/usr/bin/env python3

import os
import telebot
import requests
import logging
import time

# --- Configuracion ---
TOKEN = "7078743290:AAGpGNQnc7HSQsz31TltSzfJ4dNjUGsNlWQ" # Usa tu token real
FLASK_LLM_ENDPOINT = "http://127.0.0.1:5000/anton"
STATUS_ENDPOINT = "http://127.0.0.1:5000/status"
BOT_LOG_FILE = os.path.expanduser("~/bot.log")
EDUARD_USER_ID = 5863916279 # Reemplaza con tu user_id

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler(BOT_LOG_FILE), logging.StreamHandler()]
)

bot = telebot.TeleBot(TOKEN)

# --- Comandos del Bot ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = "🔥 **Anton Lavey IA 3.0** 🔥\n\nListo para tus instrucciones. Usa `/status` para ver el estado del sistema."
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def check_status(message):
    status_msg = bot.reply_to(message, "🔄 Verificando estado del sistema...")
    try:
        response = requests.get(STATUS_ENDPOINT, timeout=15)
        response.raise_for_status()
        status_data = response.json()
        
        # Si la petición fue exitosa (código 200), Flask está activo.
        flask_status = "✅ Activo" 
        
        # Extraemos el estado del LLM de la estructura correcta.
        server_status = status_data.get("server_status", {})
        llama_status = server_status.get("status", "❓ Inaccesible") # Usamos la clave correcta "status"
        
        response_message = f"🟢 **Estado de Anton Lavey IA:**\n\n• Servidor API (Flask): {flask_status}\n• Servidor LLM (llama.cpp): {llama_status}"
        bot.edit_message_text(response_message, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown')
    except Exception as e:
        error_msg = f"❌ **Error de Conexión**\nNo se pudo contactar al servidor: {str(e)}"
        bot.edit_message_text(error_msg, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown')

# --- Manejo de Mensajes ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_prompt = message.text
    logging.info(f"BOT_MESSAGE: Recibido: '{user_prompt}'")
    bot.send_chat_action(message.chat.id, 'typing')

    try:
        start_time = time.time()
        response = requests.post(
            FLASK_LLM_ENDPOINT,
            json={"prompt": user_prompt, "user_id": str(message.from_user.id)},
            timeout=600
        )
        processing_time = round((time.time() - start_time), 2)
        response.raise_for_status()
        
        anton_response_data = response.json()
        anton_response_text = anton_response_data.get("response", "No se obtuvo respuesta.")
        
        if processing_time > 5:
            anton_response_text += f"\n\n⏱️ *Procesado en {processing_time}s*"
        
        bot.reply_to(message, anton_response_text, parse_mode='Markdown')
    except Exception as e:
        error_msg = f"❌ Error al procesar tu solicitud: {str(e)}"
        bot.reply_to(message, error_msg, parse_mode='Markdown')
        logging.error(f"BOT_ERROR: {str(e)}")

# --- Arranque ---
if __name__ == '__main__':
    logging.info("BOT_STARTUP: Iniciando polling del bot de Telegram...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.critical(f"BOT_CRITICAL: El bot se detuvo con un error crítico: {e}")
