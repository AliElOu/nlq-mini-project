"""
Script CLI pour tester le système NLQ
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.nlq_service import NLQService
from config.settings import Config
import json

def main():
    """Interface en ligne de commande pour tester le système NLQ"""
    print("🛍️ NLQ E-commerce - Interface CLI")
    print("=" * 50)
    
    try:
        # Valider la configuration
        Config.validate()
        print("✅ Configuration validée")
        
        # Initialiser le service
        nlq_service = NLQService()
        print("✅ Service NLQ initialisé")
        
        # Afficher les statistiques de la base de données
        stats = nlq_service.get_database_stats()
        print(f"\n📊 Statistiques de la base de données:")
        for key, value in stats.items():
            print(f"  - {key}: {value}")
        
        print(f"\n💡 Suggestions de requêtes:")
        suggestions = nlq_service.get_suggestions()
        for i, suggestion in enumerate(suggestions[:5], 1):
            print(f"  {i}. {suggestion}")
        
        print(f"\n" + "=" * 50)
        print("Tapez vos requêtes en langage naturel (ou 'quit' pour quitter)")
        print("=" * 50)
        
        while True:
            try:
                query = input("\n🔍 Votre requête: ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("👋 Au revoir!")
                    break
                
                if not query:
                    continue
                
                print("⏳ Traitement en cours...")
                result = nlq_service.process_query(query)
                
                print("\n" + "=" * 50)
                if result['success']:
                    print(f"✅ Résultats trouvés: {result['count']}")
                    print(f"🤖 Réponse: {result['natural_response']}")
                    print(f"📊 Confiance: {result['confidence']:.1%}")
                    print(f"🔧 SQL: {result['sql_query']}")
                    
                    if result['data'] and len(result['data']) <= 3:
                        print(f"\n📋 Détails des résultats:")
                        for i, item in enumerate(result['data'], 1):
                            print(f"  {i}. {json.dumps(item, ensure_ascii=False, indent=4)}")
                else:
                    print(f"❌ Erreur: {result['error']}")
                    print(f"💬 {result['natural_response']}")
                
                print("=" * 50)
                
            except KeyboardInterrupt:
                print("\n👋 Au revoir!")
                break
            except Exception as e:
                print(f"❌ Erreur inattendue: {e}")
    
    except Exception as e:
        print(f"❌ Erreur d'initialisation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
