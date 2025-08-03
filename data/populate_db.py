"""
Script pour peupler la base de données avec des données de démonstration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database_manager import DatabaseManager
import random

def populate_database():
    """Peupler la base de données avec des données d'exemple"""
    db = DatabaseManager()
    
    print("Peuplement de la base de données...")
    
    # Insertion des catégories
    categories_data = [
        ("T-shirts", "T-shirts et tops pour tous", None),
        ("Pantalons", "Pantalons et jeans", None),
        ("Robes", "Robes et jupes", None),
        ("Chaussures", "Chaussures pour tous", None),
        ("Accessoires", "Sacs, ceintures et bijoux", None),
        ("T-shirts Homme", "T-shirts pour homme", 1),
        ("T-shirts Femme", "T-shirts pour femme", 1),
        ("Jeans", "Jeans et denim", 2),
        ("Pantalons Chino", "Pantalons chino", 2),
        ("Robes d'été", "Robes légères pour l'été", 3),
        ("Robes de soirée", "Robes élégantes", 3),
        ("Baskets", "Chaussures de sport", 4),
        ("Chaussures de ville", "Chaussures élégantes", 4),
    ]
    
    for name, description, parent_id in categories_data:
        db.execute_update(
            "INSERT OR IGNORE INTO categories (name, description, parent_id) VALUES (?, ?, ?)",
            (name, description, parent_id)
        )
    
    # Insertion des marques
    brands_data = [
        ("Nike", "Marque de sport américaine", "États-Unis"),
        ("Adidas", "Marque de sport allemande", "Allemagne"),
        ("Zara", "Mode fast-fashion espagnole", "Espagne"),
        ("H&M", "Mode suédoise abordable", "Suède"),
        ("Uniqlo", "Mode japonaise fonctionnelle", "Japon"),
        ("Levi's", "Marque de denim américaine", "États-Unis"),
        ("Mango", "Mode espagnole contemporaine", "Espagne"),
        ("Gap", "Mode américaine décontractée", "États-Unis"),
    ]
    
    for name, description, country in brands_data:
        db.execute_update(
            "INSERT OR IGNORE INTO brands (name, description, country) VALUES (?, ?, ?)",
            (name, description, country)
        )
    
    # Insertion des produits
    products_data = [
        # T-shirts
        ("T-shirt basique blanc", "T-shirt en coton 100% blanc unisexe", 15.99, 19.99, 6, 1, "TSH001", 50, "blanc", "M", "coton", "unisexe", "toute_saison"),
        ("T-shirt basique noir", "T-shirt en coton 100% noir unisexe", 15.99, 19.99, 6, 1, "TSH002", 45, "noir", "L", "coton", "unisexe", "toute_saison"),
        ("T-shirt Nike Dri-FIT", "T-shirt de sport Nike pour homme", 29.99, 34.99, 6, 1, "TSH003", 30, "bleu", "M", "polyester", "homme", "toute_saison"),
        ("T-shirt femme Zara", "T-shirt tendance pour femme", 12.99, 16.99, 7, 3, "TSH004", 25, "rose", "S", "coton", "femme", "printemps"),
        
        # Jeans
        ("Jean Levi's 501", "Jean classique Levi's coupe droite", 89.99, 99.99, 8, 6, "JEA001", 20, "bleu", "32", "denim", "unisexe", "toute_saison"),
        ("Jean skinny noir", "Jean skinny taille haute pour femme", 39.99, 49.99, 8, 3, "JEA002", 35, "noir", "28", "denim", "femme", "toute_saison"),
        ("Jean regular Uniqlo", "Jean coupe regular confortable", 49.99, 59.99, 8, 5, "JEA003", 40, "bleu", "30", "denim", "homme", "toute_saison"),
        
        # Robes
        ("Robe d'été fleurie", "Robe légère à motifs floraux", 35.99, 45.99, 10, 3, "ROB001", 15, "multicolore", "M", "coton", "femme", "été"),
        ("Robe de soirée noire", "Robe élégante pour soirée", 79.99, 99.99, 11, 7, "ROB002", 8, "noir", "S", "polyester", "femme", "toute_saison"),
        ("Robe casual H&M", "Robe décontractée pour tous les jours", 24.99, 29.99, 10, 4, "ROB003", 22, "blanc", "L", "coton", "femme", "printemps"),
        
        # Chaussures
        ("Baskets Nike Air Max", "Baskets de course Nike Air Max", 119.99, 139.99, 12, 1, "CHA001", 25, "blanc", "42", "synthétique", "unisexe", "toute_saison"),
        ("Baskets Adidas Stan Smith", "Baskets blanches iconiques", 89.99, 99.99, 12, 2, "CHA002", 30, "blanc", "40", "cuir", "unisexe", "toute_saison"),
        ("Chaussures de ville", "Chaussures élégantes en cuir", 69.99, 79.99, 13, 8, "CHA003", 12, "noir", "41", "cuir", "homme", "toute_saison"),
        
        # Accessoires
        ("Sac à dos Adidas", "Sac à dos de sport Adidas", 45.99, 55.99, 5, 2, "ACC001", 18, "noir", "unique", "polyester", "unisexe", "toute_saison"),
        ("Ceinture en cuir", "Ceinture classique en cuir véritable", 29.99, 39.99, 5, 8, "ACC002", 20, "marron", "85cm", "cuir", "homme", "toute_saison"),
    ]
    
    for (name, description, price, original_price, category_id, brand_id, sku, 
         stock, color, size, material, gender, season) in products_data:
        db.execute_update(
            """INSERT OR IGNORE INTO products 
               (name, description, price, original_price, category_id, brand_id, sku, 
                stock_quantity, color, size, material, gender, season, is_active) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)""",
            (name, description, price, original_price, category_id, brand_id, sku,
             stock, color, size, material, gender, season)
        )
    
    # Insertion de quelques commandes d'exemple
    orders_data = [
        ("client1@email.com", 45.98, "confirmé", "123 Rue de la Paix, Paris"),
        ("client2@email.com", 89.99, "expédié", "456 Avenue des Champs, Lyon"),
        ("client3@email.com", 159.97, "livré", "789 Boulevard Central, Marseille"),
    ]
    
    for email, total, status, address in orders_data:
        db.execute_update(
            "INSERT INTO orders (customer_email, total_amount, status, shipping_address) VALUES (?, ?, ?, ?)",
            (email, total, status, address)
        )
    
    # Insertion des articles de commandes
    order_items_data = [
        (1, 1, 2, 15.99, 31.98),  # 2 T-shirts blancs
        (1, 4, 1, 12.99, 12.99),  # 1 T-shirt femme
        (2, 5, 1, 89.99, 89.99),  # 1 Jean Levi's
        (3, 11, 1, 119.99, 119.99),  # 1 Baskets Nike
        (3, 8, 1, 35.99, 35.99),   # 1 Robe d'été
    ]
    
    for order_id, product_id, quantity, unit_price, total_price in order_items_data:
        db.execute_update(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES (?, ?, ?, ?, ?)",
            (order_id, product_id, quantity, unit_price, total_price)
        )
    
    print("Base de données peuplée avec succès!")
    
    # Afficher les statistiques
    stats = db.execute_query("SELECT COUNT(*) as count FROM products")
    print(f"Produits créés: {stats[0]['count']}")
    
    stats = db.execute_query("SELECT COUNT(*) as count FROM categories")
    print(f"Catégories créées: {stats[0]['count']}")
    
    stats = db.execute_query("SELECT COUNT(*) as count FROM brands")
    print(f"Marques créées: {stats[0]['count']}")
    
    stats = db.execute_query("SELECT COUNT(*) as count FROM orders")
    print(f"Commandes créées: {stats[0]['count']}")

if __name__ == "__main__":
    populate_database()
