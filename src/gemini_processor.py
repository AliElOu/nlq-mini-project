"""
Module d'intégration avec l'API Gemini pour la compréhension du langage naturel
"""
import google.generativeai as genai
from typing import Dict, Any, Optional
import json
import re
from config.settings import Config

class GeminiNLQProcessor:
    """Processeur de requêtes en langage naturel utilisant l'API Gemini"""
    
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Schéma de base de données pour le contexte
        self.db_schema = """
        Base de données e-commerce avec les tables suivantes:
        
        1. categories: id, name, description, parent_id
        2. brands: id, name, description, country
        3. products: id, name, description, price, original_price, category_id, brand_id, 
           sku, stock_quantity, color, size, material, gender, season, is_active
        4. orders: id, customer_email, total_amount, status, order_date, shipping_address
        5. order_items: id, order_id, product_id, quantity, unit_price, total_price
        
        Genres possibles: homme, femme, enfant, unisexe
        Saisons possibles: printemps, été, automne, hiver, toute_saison
        Statuts de commande: en_attente, confirmé, expédié, livré, annulé
        """
    
    def process_natural_query(self, user_query: str) -> Dict[str, Any]:
        """
        Traiter une requête en langage naturel et générer une requête SQL
        
        Args:
            user_query: La requête de l'utilisateur en langage naturel
            
        Returns:
            Dictionnaire contenant la requête SQL et les métadonnées
        """
        prompt = f"""
        Tu es un expert en SQL pour une base de données e-commerce de vêtements.
        
        {self.db_schema}
        
        Convertis cette requête en langage naturel en une requête SQL valide:
        "{user_query}"
        
        Règles importantes:
        1. Génère UNIQUEMENT une requête SELECT
        2. Utilise des JOINs appropriés quand nécessaire
        3. Limite les résultats à 50 maximum
        4. Assure-toi que la requête est sécurisée (pas d'injection SQL)
        5. Utilise des noms de colonnes clairs dans le SELECT
        6. Si la requête concerne les prix, assure-toi d'utiliser la colonne 'price'
        7. Pour les recherches de texte, utilise LIKE avec des wildcards appropriés
        
        Réponds UNIQUEMENT avec un JSON valide contenant:
        {{
            "sql_query": "la requête SQL générée",
            "explanation": "explication de ce que fait la requête",
            "filters_applied": ["liste des filtres appliqués"],
            "confidence": "niveau de confiance entre 0 et 1"
        }}
        
        Ne génère aucun autre texte en dehors du JSON.
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Nettoyer la réponse pour extraire le JSON
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                json_text = json_match.group()
                result = json.loads(json_text)
                
                # Validation de la requête SQL
                if self._validate_sql_query(result.get('sql_query', '')):
                    return result
                else:
                    raise ValueError("Requête SQL non valide générée")
            else:
                raise ValueError("Format de réponse JSON non valide")
                
        except Exception as e:
            return {
                "sql_query": "",
                "explanation": f"Erreur lors du traitement: {str(e)}",
                "filters_applied": [],
                "confidence": 0.0,
                "error": str(e)
            }
    
    def _validate_sql_query(self, sql_query: str) -> bool:
        """
        Valider une requête SQL pour s'assurer qu'elle est sécurisée
        
        Args:
            sql_query: La requête SQL à valider
            
        Returns:
            True si la requête est valide, False sinon
        """
        if not sql_query:
            return False
        
        # Vérifications de sécurité de base
        sql_lower = sql_query.lower().strip()
        
        # Doit commencer par SELECT
        if not sql_lower.startswith('select'):
            return False
        
        # Ne doit pas contenir de mots-clés dangereux
        dangerous_keywords = [
            'drop', 'delete', 'insert', 'update', 'alter', 'create',
            'truncate', 'exec', 'execute', 'union', '--'
        ]
        
        for keyword in dangerous_keywords:
            if keyword in sql_lower:
                return False
        
        return True
    
    def generate_natural_response(self, query_result: Dict[str, Any], 
                                original_query: str) -> str:
        """
        Générer une réponse en langage naturel à partir des résultats de la requête
        
        Args:
            query_result: Résultats de la requête SQL
            original_query: Requête originale de l'utilisateur
            
        Returns:
            Réponse en langage naturel
        """
        if 'error' in query_result:
            return f"Désolé, je n'ai pas pu traiter votre demande: {query_result['error']}"
        
        data = query_result.get('data', [])
        if not data:
            return "Aucun résultat trouvé pour votre recherche."
        
        prompt = f"""
        Tu es un assistant e-commerce expert. 
        
        L'utilisateur a demandé: "{original_query}"
        
        Voici les résultats trouvés (au format JSON):
        {json.dumps(data[:5], ensure_ascii=False, indent=2)}
        
        Nombre total de résultats: {len(data)}
        
        Génère une réponse naturelle et utile qui:
        1. Résume les résultats trouvés
        2. Mentionne les informations les plus pertinentes (prix, marques, etc.)
        3. Suggère d'autres recherches si pertinent
        4. Reste concise mais informative
        
        Réponds en français de manière naturelle et engageante.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Voici les résultats de votre recherche: {len(data)} produit(s) trouvé(s)."
