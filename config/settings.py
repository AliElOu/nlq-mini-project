"""
Configuration module for NLQ E-commerce system
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Config:
    """Configuration principale de l'application"""
    
    # API Configuration
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Database Configuration
    DATABASE_PATH = os.getenv("DATABASE_PATH", "./database/ecommerce.db")
    
    # Application Configuration
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "localhost")
    PORT = int(os.getenv("PORT", 8000))
    
    # NLQ Configuration
    MAX_QUERY_LENGTH = 500
    DEFAULT_LIMIT = 10
    
    @classmethod
    def validate(cls):
        """Valider la configuration"""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY n'est pas définie dans les variables d'environnement")
        
        if not os.path.exists(os.path.dirname(cls.DATABASE_PATH)):
            os.makedirs(os.path.dirname(cls.DATABASE_PATH), exist_ok=True)
