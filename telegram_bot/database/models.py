import pymysql
from pymysql import Error
import logging
from config.settings import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

def get_db_connection():
    """Create a database connection."""
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            connect_timeout=10,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        logging.info("Successfully connected to MySQL database")
        return connection
    except Error as e:
        logging.error(f"Error connecting to MySQL: {e}")
        return None

def init_db():
    """Initialize the database with required tables."""
    connection = None
    cursor = None
    try:
        connection = get_db_connection()
        if connection is None:
            return

        cursor = connection.cursor()
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(255),
                user_name VARCHAR(255),
                message TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_messages_user_id (user_id),
                INDEX idx_messages_timestamp (timestamp)
            )
        ''')
        
        # User activity table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_activity (
                user_id VARCHAR(255) PRIMARY KEY,
                message_count INT DEFAULT 0,
                last_message_time DATETIME
            )
        ''')
        
        connection.commit()
        logging.info("Database tables created successfully")
        
    except Error as e:
        logging.error(f"Error creating tables: {e}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close() 