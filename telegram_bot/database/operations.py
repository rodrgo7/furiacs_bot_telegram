from datetime import datetime, timedelta
import logging
from config.settings import MESSAGE_LIMIT, MESSAGE_RETENTION_DAYS
from utils.encryption import encryptor
from .models import get_db_connection

def save_message(user_id, user_name, message):
    """Save an encrypted message to the database."""
    connection = None
    cursor = None
    try:
        encrypted_msg = encryptor.encrypt(message)
        connection = get_db_connection()
        if connection is None:
            logging.error("Failed to connect to database")
            return

        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO messages (user_id, user_name, message) VALUES (%s, %s, %s)",
            (user_id, user_name, encrypted_msg)
        )
        connection.commit()
    except Exception as e:
        logging.error(f"Erro ao salvar mensagem: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def check_message_limit(user_id):
    """Check if user has exceeded message limit."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection is None:
            logging.error("Failed to connect to database")
            return False

        cursor = connection.cursor()
        cursor.execute(
            "SELECT message_count, last_message_time FROM user_activity WHERE user_id = %s",
            (user_id,)
        )
        result = cursor.fetchone()
        now = datetime.now()
        
        if result:
            count = result['message_count']
            last_time = result['last_message_time']
            if (now - last_time) > timedelta(minutes=1):
                cursor.execute(
                    "UPDATE user_activity SET message_count = 1, last_message_time = %s WHERE user_id = %s",
                    (now, user_id)
                )
                connection.commit()
                return True
            elif count < MESSAGE_LIMIT:
                cursor.execute(
                    "UPDATE user_activity SET message_count = message_count + 1, last_message_time = %s WHERE user_id = %s",
                    (now, user_id)
                )
                connection.commit()
                return True
            return False
        else:
            cursor.execute(
                "INSERT INTO user_activity (user_id, message_count, last_message_time) VALUES (%s, 1, %s)",
                (user_id, now)
            )
            connection.commit()
            return True
    except Exception as e:
        logging.error(f"Erro ao verificar limite de mensagens: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def get_recent_chat_history(limit=50):
    """Get recent chat history with decrypted messages."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection is None:
            logging.error("Failed to connect to database")
            return "Erro ao conectar ao banco de dados."

        cursor = connection.cursor()
        cursor.execute("""
            SELECT user_name, message, timestamp 
            FROM messages 
            ORDER BY timestamp DESC
            LIMIT %s
        """, (limit,))
        
        messages = []
        for row in cursor.fetchall():
            try:
                decrypted_msg = encryptor.decrypt(row['message'])
                messages.append({
                    'user_name': row['user_name'],
                    'message': decrypted_msg,
                    'timestamp': row['timestamp']
                })
            except:
                continue
        
        if not messages:
            return "Nenhuma mensagem recente no chat."
            
        history = "📜 Últimas mensagens:\n\n"
        for msg in reversed(messages):
            history += f"🗨️ **{msg['user_name']}** ({msg['timestamp']}): {msg['message']}\n"
            
        return history
    except Exception as e:
        logging.error(f"Erro ao buscar histórico: {e}")
        return "Erro ao carregar histórico."
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def clean_old_messages():
    """Remove messages older than retention period."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection is None:
            logging.error("Failed to connect to database")
            return

        cursor = connection.cursor()
        cursor.execute(
            "DELETE FROM messages WHERE timestamp < DATE_SUB(NOW(), INTERVAL %s DAY)",
            (MESSAGE_RETENTION_DAYS,)
        )
        connection.commit()
        logging.info("Mensagens antigas removidas")
    except Exception as e:
        logging.error(f"Erro ao limpar mensagens: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def delete_user_data(user_id):
    """Delete all data associated with a user."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection is None:
            logging.error("Failed to connect to database")
            return False

        cursor = connection.cursor()
        cursor.execute("DELETE FROM messages WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM user_activity WHERE user_id = %s", (user_id,))
        connection.commit()
        return True
    except Exception as e:
        logging.error(f"Erro ao deletar dados: {e}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close() 