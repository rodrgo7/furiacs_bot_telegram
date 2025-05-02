import re
from typing import List, Set
import os
import logging

# Cria o logger
logger = logging.getLogger('FuriaBot')

class WordFilter:
    def __init__(self):
        # Carrega palavras ofensivas do arquivo
        self.offensive_words: Set[str] = set()
        self.load_words_from_file()
        logger.info(f"Word filter initialized with words: {self.offensive_words}")
    
    def load_words_from_file(self) -> None:
        """Load offensive words from the bads_word file."""
        try:
            file_path = os.path.join(os.path.dirname(__file__), 'bads_word')
            logger.info(f"Loading bad words from: {file_path}")
            
            if not os.path.exists(file_path):
                logger.error(f"Bad words file not found at: {file_path}")
                return
            
            with open(file_path, 'r', encoding='utf-8') as file:
                words = file.read().splitlines()
                # Filtrar linhas e comentários vazios
                self.offensive_words = {word.strip().lower() for word in words 
                                     if word.strip() and not word.strip().startswith('#')}
                logger.info(f"Loaded {len(self.offensive_words)} words from file")
                logger.info(f"Loaded words: {self.offensive_words}")
        except Exception as e:
            logger.error(f"Error loading bad words file: {e}")
            self.offensive_words = set()
    
    def filter_message(self, message: str) -> str:
        """
        Replace offensive words with ****.
        
        Args:
            message (str): The message to filter
            
        Returns:
            str: Filtered message with offensive words replaced by ****
        """
        original_message = message
        filtered_message = message
        
        logger.info(f"Filtering message: {message}")
        logger.info(f"Current offensive words: {self.offensive_words}")
        
        words = message.split()
        filtered_words = []
        
        for word in words:
            word_lower = word.lower()
            if word_lower in self.offensive_words:
                logger.info(f"Found offensive word: {word}")
                filtered_words.append("****")
            else:
                filtered_words.append(word)
        
        filtered_message = " ".join(filtered_words)
        
        # Log the results
        if filtered_message != original_message:
            logger.info(f"Original message: {original_message}")
            logger.info(f"Filtered message: {filtered_message}")
        
        return filtered_message
    
    def add_word(self, word: str) -> None:
        """Add a new word to the filter list."""
        self.offensive_words.add(word.lower())
        logger.info(f"Added word to filter: {word}")
        logger.info(f"Current word list: {self.offensive_words}")
    
    def remove_word(self, word: str) -> None:
        """Remove a word from the filter list."""
        self.offensive_words.discard(word.lower())
        logger.info(f"Removed word from filter: {word}")
        logger.info(f"Current word list: {self.offensive_words}")

word_filter = WordFilter()