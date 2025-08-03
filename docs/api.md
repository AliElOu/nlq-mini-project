# Documentation API

## Vue d'ensemble

L'API NLQ E-commerce permet de traiter des requêtes en langage naturel sur une base de données e-commerce de vêtements.

## Endpoints

### POST /query

Traite une requête en langage naturel et retourne les résultats.

**Request Body:**
```json
{
    "query": "Montre-moi tous les t-shirts pour homme en coton",
    "limit": 10
}
```

**Response:**
```json
{
    "success": true,
    "data": [...],
    "sql_query": "SELECT ...",
    "explanation": "Cette requête recherche...",
    "filters_applied": ["genre: homme", "matière: coton"],
    "confidence": 0.95,
    "natural_response": "J'ai trouvé 5 t-shirts pour homme en coton...",
    "count": 5
}
```

### GET /suggestions

Retourne des suggestions de requêtes d'exemple.

**Response:**
```json
{
    "suggestions": [
        "Montre-moi tous les t-shirts pour homme en coton",
        "Quels sont les produits en promotion?",
        ...
    ]
}
```

### GET /stats

Retourne des statistiques sur la base de données.

**Response:**
```json
{
    "active_products": 15,
    "categories": 13,
    "brands": 8,
    "orders": 3
}
```

### GET /health

Vérifie l'état de l'API.

**Response:**
```json
{
    "status": "OK",
    "message": "NLQ E-commerce API is running"
}
```

## Exemples de requêtes

### Recherche de produits

- `"Montre-moi tous les t-shirts pour homme en coton"`
- `"Trouve des robes d'été de moins de 50 euros"`
- `"Affiche les produits Nike disponibles"`
- `"Quels sont les jeans Levi's en stock?"`

### Requêtes sur les prix

- `"Quels sont les produits en promotion?"`
- `"Trouve les articles les moins chers"`
- `"Montre-moi les produits entre 20 et 50 euros"`

### Requêtes par catégorie

- `"Affiche toutes les chaussures disponibles"`
- `"Montre-moi les accessoires"`
- `"Quels sont les vêtements d'hiver?"`

### Requêtes sur les commandes

- `"Quelles sont les ventes de cette semaine?"`
- `"Affiche les commandes en cours"`
- `"Montre-moi les produits les plus vendus"`

## Codes d'erreur

- `400` : Requête invalide
- `500` : Erreur serveur interne
- `422` : Erreur de validation des données

## Limites

- Longueur maximale des requêtes : 500 caractères
- Limite par défaut des résultats : 10
- Seules les requêtes SELECT sont autorisées pour des raisons de sécurité
