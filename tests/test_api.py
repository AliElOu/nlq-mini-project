"""
Tests d'intégration pour l'API
"""
import unittest
import requests
import json
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestAPIIntegration(unittest.TestCase):
    """Tests d'intégration pour l'API FastAPI"""
    
    BASE_URL = "http://localhost:8000"
    
    @classmethod
    def setUpClass(cls):
        """Vérifier que l'API est accessible"""
        try:
            response = requests.get(f"{cls.BASE_URL}/health", timeout=5)
            if response.status_code != 200:
                raise Exception("API non accessible")
        except Exception as e:
            print(f"Erreur: L'API doit être démarrée sur {cls.BASE_URL}")
            print("Exécutez 'python main.py' dans un autre terminal")
            raise unittest.SkipTest(f"API non disponible: {e}")
    
    def test_health_endpoint(self):
        """Test de l'endpoint de santé"""
        response = requests.get(f"{self.BASE_URL}/health")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "OK")
    
    def test_stats_endpoint(self):
        """Test de l'endpoint des statistiques"""
        response = requests.get(f"{self.BASE_URL}/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("active_products", data)
        self.assertIsInstance(data["active_products"], int)
    
    def test_suggestions_endpoint(self):
        """Test de l'endpoint des suggestions"""
        response = requests.get(f"{self.BASE_URL}/suggestions")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("suggestions", data)
        self.assertIsInstance(data["suggestions"], list)
        self.assertGreater(len(data["suggestions"]), 0)
    
    def test_query_endpoint_valid(self):
        """Test de l'endpoint de requête avec une requête valide"""
        query_data = {
            "query": "Montre-moi tous les produits",
            "limit": 5
        }
        response = requests.post(
            f"{self.BASE_URL}/query",
            json=query_data,
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("success", False))
        self.assertIn("natural_response", data)
    
    def test_query_endpoint_empty(self):
        """Test de l'endpoint de requête avec une requête vide"""
        query_data = {"query": ""}
        response = requests.post(
            f"{self.BASE_URL}/query",
            json=query_data,
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data.get("success", True))
    
    def test_home_page(self):
        """Test de la page d'accueil"""
        response = requests.get(f"{self.BASE_URL}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("text/html", response.headers.get("content-type", ""))

if __name__ == "__main__":
    unittest.main()
