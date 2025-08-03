"""
Module de gestion de la base de données SQLite pour l'e-commerce
"""
import sqlite3
import os
from typing import List, Dict, Any, Optional
from config.settings import Config

class DatabaseManager:
    """Gestionnaire de base de données pour le système e-commerce"""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or Config.DATABASE_PATH
        self.ensure_database_exists()
        self.init_tables()
    
    def ensure_database_exists(self):
        """S'assurer que le répertoire de la base de données existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtenir une connexion à la base de données"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Pour avoir des résultats sous forme de dictionnaire
        return conn
    
    def init_tables(self):
        """Initialiser les tables de la base de données"""
        with self.get_connection() as conn:
            # Table des catégories
            conn.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    description TEXT,
                    parent_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (parent_id) REFERENCES categories (id)
                )
            """)
            
            # Table des marques
            conn.execute("""
                CREATE TABLE IF NOT EXISTS brands (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL UNIQUE,
                    description TEXT,
                    country VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des produits
            conn.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(200) NOT NULL,
                    description TEXT,
                    price DECIMAL(10, 2) NOT NULL,
                    original_price DECIMAL(10, 2),
                    category_id INTEGER NOT NULL,
                    brand_id INTEGER,
                    sku VARCHAR(50) UNIQUE,
                    stock_quantity INTEGER DEFAULT 0,
                    color VARCHAR(50),
                    size VARCHAR(20),
                    material VARCHAR(100),
                    gender ENUM('homme', 'femme', 'enfant', 'unisexe') DEFAULT 'unisexe',
                    season ENUM('printemps', 'été', 'automne', 'hiver', 'toute_saison') DEFAULT 'toute_saison',
                    is_active BOOLEAN DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories (id),
                    FOREIGN KEY (brand_id) REFERENCES brands (id)
                )
            """)
            
            # Table des commandes
            conn.execute("""
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_email VARCHAR(255) NOT NULL,
                    total_amount DECIMAL(10, 2) NOT NULL,
                    status ENUM('en_attente', 'confirmé', 'expédié', 'livré', 'annulé') DEFAULT 'en_attente',
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    shipping_address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Table des articles de commande
            conn.execute("""
                CREATE TABLE IF NOT EXISTS order_items (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    order_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price DECIMAL(10, 2) NOT NULL,
                    total_price DECIMAL(10, 2) NOT NULL,
                    FOREIGN KEY (order_id) REFERENCES orders (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            """)
            
            conn.commit()
    
    def execute_query(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Exécuter une requête SELECT et retourner les résultats"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: tuple = ()) -> int:
        """Exécuter une requête UPDATE/INSERT/DELETE et retourner le nombre de lignes affectées"""
        with self.get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def get_table_schema(self, table_name: str) -> List[Dict[str, Any]]:
        """Obtenir le schéma d'une table"""
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def get_all_tables(self) -> List[str]:
        """Obtenir la liste de toutes les tables"""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        result = self.execute_query(query)
        return [row['name'] for row in result]
