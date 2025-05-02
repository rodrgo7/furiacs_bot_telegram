from telethon import TelegramClient, events
from telethon.tl.types import PeerUser
import asyncio
import logging
import sys
from datetime import datetime, timedelta

# Configurar o registro
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log')
    ]
)

# Criar logger
logger = logging.getLogger('FuriaBot')

from config.settings import API_ID, API_HASH, BOT_TOKEN
from config.menus import MAIN_MENU, COMMUNITY_MENU, SOCIAL_MEDIA_MENU, ROSTER_MENU
from database.models import init_db
from database.operations import (
    save_message, check_message_limit, get_recent_chat_history,
    clean_old_messages, delete_user_data
)
from services.news_service import get_most_recent_news
from utils.word_filter import word_filter

# Inicia bot
bot = TelegramClient('furia_bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

active_chats = {}

# Mensagem de boas-vindas e regras
WELCOME_MESSAGE = (
    "📌 *Regras do Grupo* 📌\n\n"
    "Bem-vindo(a) ao nosso grupo! Para manter um ambiente saudável e agradável para todos, siga estas regras:\n\n"
    "1️⃣ *Respeito acima de tudo* – Trate todos os membros com respeito e educação. Não serão toleradas ofensas, discursos de ódio ou atitudes discriminatórias.\n\n"
    "2️⃣ *Nada de spam ou publicidade* – Postagens repetitivas, links de divulgação sem permissão e propagandas não autorizadas serão removidas.\n\n"
    "3️⃣ *Conteúdo apropriado* – Não compartilhe material impróprio, ofensivo, ilegal ou que viole as diretrizes do Telegram.\n\n"
    "4️⃣ *Evite conflitos* – Discussões são bem-vindas, mas mantenha o bom senso. Se houver desentendimentos, resolvam de forma madura.\n\n"
    "5️⃣ *Siga as diretrizes do grupo* – Admins podem adicionar regras específicas conforme necessário. Fique atento(a) às notificações e comunicados.\n\n"
    "⚠️ O não cumprimento das regras pode resultar em advertências ou até remoção do grupo.\n\n"
    "Aproveite sua estadia e participe com respeito e colaboração!\n\n"
    "👊 *Bem-vindo ao FURIA CS Fans Bot!*"
)

async def broadcast_message(message, sender=None):
    """Broadcast a message to all active chats."""
    for user_id in active_chats:
        try:
            if sender and user_id == sender.id:
                continue
            await bot.send_message(
                user_id,
                f"🗨️ **{sender.first_name}:** {message}" if sender else message,
                parse_mode='markdown'
            )
        except Exception as e:
            logger.error(f"Erro ao enviar para {user_id}: {e}")
            if "privacy settings" in str(e):
                active_chats.pop(user_id, None)

async def clean_inactive_chats():
    """Clean up inactive chat sessions."""
    while True:
        await asyncio.sleep(300)  # Verificar a cada 5 minutos
        now = datetime.now()
        inactive = [uid for uid, last_active in active_chats.items() 
                   if (now - last_active) > timedelta(minutes=30)]
        for uid in inactive:
            active_chats.pop(uid, None)
            try:
                await bot.send_message(uid, "Você foi desconectado do chat por inatividade.")
            except:
                pass

async def periodic_tasks():
    """Run periodic maintenance tasks."""
    while True:
        await asyncio.sleep(86400)  # 24 horas
        clean_old_messages()
        await clean_inactive_chats()

# Event Handlers
@bot.on(events.NewMessage(pattern='/start'))
async def start(event):
    logger.info(f"User {event.sender_id} started the bot")
    await event.respond(
        WELCOME_MESSAGE,
        buttons=MAIN_MENU,
        parse_mode='markdown'
    )

@bot.on(events.CallbackQuery)
async def handle_buttons(event):
    logger.info(f"Button pressed: {event.data} by user {event.sender_id}")
    if event.data == b"news":
        news = get_most_recent_news()
        await event.edit(news, buttons=MAIN_MENU)
    
    elif event.data == b"highlights":
        await event.edit("🎥 Destaques recentes (em breve!)", buttons=MAIN_MENU)
    
    elif event.data == b"ranking":
        await event.edit("👊 FURIA está na 17ª posição do ranking mundial.", buttons=MAIN_MENU)
    
    elif event.data == b"roster":
        await event.respond("👥 Elenco atual:", buttons=ROSTER_MENU)
    
    elif event.data == b"community":
        await event.edit("💬 Comunidade FURIA:", buttons=COMMUNITY_MENU)
    
    elif event.data == b"fan_chat":
        user = await event.get_sender()
        active_chats[user.id] = datetime.now()
        logger.info(f"User {user.id} joined the chat")
        
        chat_history = get_recent_chat_history()
        
        await event.respond(
            f"💬 Você entrou no chat dos fãs!\n\n"
            f"{chat_history}\n\n"
            "Escreva aqui para conversar com outros fãs em tempo real.\n"
            "Use /exit para sair do chat.",
            buttons=COMMUNITY_MENU,
            parse_mode='markdown'
        )
        await broadcast_message(f"{user.first_name} entrou no chat!")
    
    elif event.data == b"social_media":
        await event.edit("📱 Redes Sociais:", buttons=SOCIAL_MEDIA_MENU)
    
    elif event.data == b"back":
        await event.edit("👊 Menu Principal:", buttons=MAIN_MENU)
    
    elif event.data == b"back_community":
        await event.edit("💬 Comunidade FURIA:", buttons=COMMUNITY_MENU)

@bot.on(events.NewMessage(pattern='/exit'))
async def exit_chat(event):
    user = await event.get_sender()
    active_chats.pop(user.id, None)
    logger.info(f"User {user.id} left the chat")
    await event.respond("Você saiu do chat. Use /chat para voltar quando quiser!")
    await broadcast_message(f"{user.first_name} saiu do chat.")

@bot.on(events.NewMessage(pattern='/delete_my_data'))
async def delete_my_data(event):
    user = await event.get_sender()
    logger.info(f"User {user.id} requested data deletion")
    if delete_user_data(user.id):
        await event.respond("✅ Seus dados foram removidos com sucesso!", buttons=MAIN_MENU)
    else:
        await event.respond("⚠️ Erro ao remover dados. Tente novamente.", buttons=MAIN_MENU)

@bot.on(events.NewMessage)
async def handle_chat_message(event):
    if event.message.text.startswith('/') or not isinstance(event.message.peer_id, PeerUser):
        return
    
    user = await event.get_sender()
    if user.id not in active_chats:
        return
    
    if not check_message_limit(user.id):
        logger.warning(f"User {user.id} exceeded message limit")
        await event.respond(f"⚠️ Limite de mensagens por minuto atingido!")
        return
    
    # Filtrar palavras ofensivas
    original_message = event.message.text
    filtered_message = word_filter.filter_message(original_message)
    
    # Log da mensagem e usuario
    logger.info(f"Processing message from user {user.id}")
    logger.info(f"Original message: {original_message}")
    logger.info(f"Filtered message: {filtered_message}")
    
    # Salvar e transmitir a mensagem filtrada
    save_message(user.id, user.first_name, filtered_message)
    await broadcast_message(filtered_message, user)

if __name__ == "__main__":
    # Initialize database
    logger.info("Initializing database...")
    init_db()
    clean_old_messages()
    
    logger.info("Starting periodic tasks...")
    bot.loop.create_task(periodic_tasks())
    bot.loop.create_task(clean_inactive_chats())
    
    logger.info("Bot started successfully!")
    
    # Run the bot
    bot.run_until_disconnected()
    logger.info("Bot disconnected.")
    bot.disconnect()

word_filter.add_word("new_bad_word")
word_filter.remove_word("word_to_remove")