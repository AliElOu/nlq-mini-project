"""
Tests unitaires pour le système NLQ E-commerce
"""
import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database_manager import DatabaseManager
from src.nlq_service import NLQService
from config.settings import Config

class TestDatabaseManager(unittest.TestCase):
    """Tests pour le gestionnaire de base de données"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.db = DatabaseManager(":memory:")  # Base de données en mémoire pour les tests
    
    def test_table_creation(self):
        """Tester la création des tables"""
        tables = self.db.get_all_tables()
        expected_tables = ['categories', 'brands', 'products', 'orders', 'order_items']
        
        for table in expected_tables:
            self.assertIn(table, tables)
    
    def test_insert_and_query(self):
        """Tester l'insertion et la requête de données"""
        # Insérer une catégorie
        self.db.execute_update(
            "INSERT INTO categories (name, description) VALUES (?, ?)",
            ("Test Category", "Description de test")
        )
        
        # Vérifier l'insertion
        result = self.db.execute_query("SELECT * FROM categories WHERE name = ?", ("Test Category",))
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['name'], "Test Category")

class TestNLQService(unittest.TestCase):
    """Tests pour le service NLQ"""
    
    def setUp(self):
        """Configuration avant chaque test"""
        # Note: Ces tests nécessitent une clé API Gemini valide
        self.service = NLQService()
    
    def test_empty_query(self):
        """Tester une requête vide"""
        result = self.service.process_query("")
        self.assertFalse(result['success'])
        self.assertIn("vide", result['error'].lower())
    
    def test_long_query(self):
        """Tester une requête trop longue"""
        long_query = "a" * (Config.MAX_QUERY_LENGTH + 1)
        result = self.service.process_query(long_query)
        self.assertFalse(result['success'])
        self.assertIn("longue", result['error'].lower())
    
    def test_suggestions(self):
        """Tester l'obtention de suggestions"""
        suggestions = self.service.get_suggestions()
        self.assertIsInstance(suggestions, list)
        self.assertGreater(len(suggestions), 0)

if __name__ == "__main__":
    unittest.main()
