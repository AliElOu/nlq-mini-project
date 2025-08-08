"""
Service principal pour le traitement des requêtes NLQ
"""
from typing import Dict, Any, List
from src.database_manager import DatabaseManager
from src.gemini_processor import GeminiNLQProcessor
from config.settings import Config

class NLQService:
    """Service principal pour traiter les requêtes en langage naturel"""
    
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.nlq_processor = GeminiNLQProcessor()
    
    def process_query(self, user_query: str) -> Dict[str, Any]:
        """
        Traiter une requête utilisateur complète
        
        Args:
            user_query: Requête de l'utilisateur en langage naturel
            
        Returns:
            Dictionnaire contenant les résultats et métadonnées
        """
        # Validation de la requête
        if not user_query or len(user_query.strip()) == 0:
            return {
                "success": False,
                "error": "Requête vide",
                "data": [],
                "natural_response": "Veuillez saisir une requête valide."
            }
        
        if len(user_query) > Config.MAX_QUERY_LENGTH:
            return {
                "success": False,
                "error": "Requête trop longue",
                "data": [],
                "natural_response": f"Votre requête dépasse la limite de {Config.MAX_QUERY_LENGTH} caractères."
            }
        
        try:
            # 1. Traiter la requête avec Gemini
            nlq_result = self.nlq_processor.process_natural_query(user_query)
            
            if 'error' in nlq_result:
                return {
                    "success": False,
                    "error": nlq_result['error'],
                    "data": [],
                    "natural_response": "Je n'ai pas pu comprendre votre requête. Pouvez-vous la reformuler?"
                }
            
            # 2. Exécuter la requête SQL
            sql_query = nlq_result.get('sql_query', '')
            if not sql_query:
                return {
                    "success": False,
                    "error": "Aucune requête SQL générée",
                    "data": [],
                    "natural_response": "Je n'ai pas pu générer une requête appropriée."
                }
            
            # Exécuter la requête
            query_results = self.db_manager.execute_query(sql_query)
            
            # 3. Générer une réponse naturelle
            result_data = {
                "data": query_results,
                "sql_query": sql_query,
                "explanation": nlq_result.get('explanation', ''),
                "filters_applied": nlq_result.get('filters_applied', []),
                "confidence": nlq_result.get('confidence', 0.0)
            }
            
            natural_response = self.nlq_processor.generate_natural_response(
                result_data, user_query
            )
            
            return {
                "success": True,
                "data": query_results,
                "sql_query": sql_query,
                "explanation": nlq_result.get('explanation', ''),
                "filters_applied": nlq_result.get('filters_applied', []),
                "confidence": nlq_result.get('confidence', 0.0),
                "natural_response": natural_response,
                "count": len(query_results)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "data": [],
                "natural_response": "Une erreur s'est produite lors du traitement de votre requête."
            }
    
    def get_suggestions(self) -> List[str]:
        """Obtenir des suggestions de requêtes exemple"""
        return [
            "Montre-moi tous les t-shirts pour homme en coton",
            "Quels sont les produits en promotion?",
            "Trouve des robes d'été de moins de 50 euros",
            "Affiche les produits Nike disponibles",
            "Trouve des chaussures pour femme en cuir",
            "Quels sont les nouveaux produits?",
            "Trouve des vêtements d'hiver pour enfant",
            "Montre-moi les produits les moins chers",
            "Quelles sont les meilleures ventes?",
            "Trouve des accessoires pour homme"
        ]
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Obtenir des statistiques sur la base de données"""
        try:
            stats = {}
            
            # Nombre de produits
            products_count = self.db_manager.execute_query(
                "SELECT COUNT(*) as count FROM products WHERE is_active = 1"
            )
            stats['active_products'] = products_count[0]['count'] if products_count else 0
            
            # Nombre de catégories
            categories_count = self.db_manager.execute_query(
                "SELECT COUNT(*) as count FROM categories"
            )
            stats['categories'] = categories_count[0]['count'] if categories_count else 0
            
            # Nombre de marques
            brands_count = self.db_manager.execute_query(
                "SELECT COUNT(*) as count FROM brands"
            )
            stats['brands'] = brands_count[0]['count'] if brands_count else 0
            
            # Nombre de commandes
            orders_count = self.db_manager.execute_query(
                "SELECT COUNT(*) as count FROM orders"
            )
            stats['orders'] = orders_count[0]['count'] if orders_count else 0
            
            return stats
            
        except Exception as e:
            return {"error": str(e)}
