# NLQ E-commerce

Un système de requêtes en langage naturel (NLQ) pour une base de données e-commerce de vêtements, utilisant l'API Gemini de Google pour la compréhension du langage naturel et SQLite pour le stockage des données.

## 🚀 Fonctionnalités

- **Requêtes en langage naturel** : Posez des questions en français comme "Montre-moi tous les t-shirts pour homme en coton"
- **Traitement intelligent** : Utilise l'API Gemini pour comprendre et convertir les requêtes en SQL
- **Base de données e-commerce** : Système complet avec produits, catégories, marques, commandes
- **API REST** : Interface FastAPI avec documentation automatique
- **Interface web** : Interface simple pour tester les requêtes
- **Réponses naturelles** : Génération de réponses en langage naturel à partir des résultats

## 📁 Structure du projet

```
nlq-mini-project/
├── src/                          # Code source principal
│   ├── __init__.py
│   ├── database_manager.py       # Gestionnaire de base de données SQLite
│   ├── gemini_processor.py       # Traitement avec l'API Gemini
│   └── nlq_service.py           # Service principal NLQ
├── config/                       # Configuration
│   └── settings.py              # Paramètres de l'application
├── database/                     # Base de données SQLite
├── data/                        # Scripts de données
│   └── populate_db.py           # Script pour peupler la DB
├── tests/                       # Tests unitaires
│   └── test_nlq.py
├── docs/                        # Documentation
├── main.py                      # Application FastAPI principale
├── requirements.txt             # Dépendances Python
├── .env.example                 # Exemple de configuration
└── README.md
```

## 🛠️ Installation

1. **Cloner le projet**
   ```bash
   git clone <repository-url>
   cd nlq-mini-project
   ```

2. **Créer un environnement virtuel**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # ou source venv/bin/activate  # Linux/Mac
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurer les variables d'environnement**
   ```bash
   cp .env.example .env
   ```
   Éditer le fichier `.env` et ajouter votre clé API Gemini :
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   DATABASE_PATH=./database/ecommerce.db
   ```

5. **Peupler la base de données**
   ```bash
   python data/populate_db.py
   ```

## 🚀 Utilisation

### Démarrer l'application

```bash
python main.py
```

L'application sera accessible à l'adresse : http://localhost:8000

### Interface web

Ouvrez votre navigateur et allez à http://localhost:8000 pour accéder à l'interface de test.

### API REST

- **Documentation API** : http://localhost:8000/docs
- **Endpoint principal** : `POST /query`
- **Statistiques** : `GET /stats`
- **Suggestions** : `GET /suggestions`

### Exemples de requêtes

```
- "Montre-moi tous les t-shirts pour homme en coton"
- "Quels sont les produits en promotion?"
- "Trouve des robes d'été de moins de 50 euros"
- "Affiche les produits Nike disponibles"
- "Quelles sont les ventes de cette semaine?"
- "Montre-moi les produits les plus vendus"
- "Trouve des chaussures pour femme en cuir"
- "Quels sont les nouveaux produits?"
```

## 🧪 Tests

Exécuter les tests unitaires :

```bash
python -m pytest tests/ -v
```

Ou directement :

```bash
python tests/test_nlq.py
```

## 📊 Base de données

### Schéma

Le système utilise une base de données SQLite avec les tables suivantes :

- **categories** : Catégories de produits (hiérarchiques)
- **brands** : Marques de produits
- **products** : Produits avec détails (prix, couleur, taille, matière, etc.)
- **orders** : Commandes clients
- **order_items** : Articles dans les commandes

### Données d'exemple

Le script `data/populate_db.py` crée des données d'exemple incluant :
- 15+ produits variés (t-shirts, jeans, robes, chaussures, accessoires)
- 8 marques (Nike, Adidas, Zara, H&M, Uniqlo, Levi's, Mango, Gap)
- Catégories hiérarchiques
- Commandes d'exemple

## 🔧 Configuration

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `GEMINI_API_KEY` | Clé API Google Gemini | **Obligatoire** |
| `DATABASE_PATH` | Chemin vers la base SQLite | `./database/ecommerce.db` |
| `DEBUG` | Mode debug | `False` |
| `HOST` | Hôte du serveur | `localhost` |
| `PORT` | Port du serveur | `8000` |

### Paramètres de l'application

- `MAX_QUERY_LENGTH` : Longueur maximale des requêtes (500 caractères)
- `DEFAULT_LIMIT` : Limite par défaut des résultats (10)

## 🔍 Comment ça marche

1. **Requête utilisateur** : L'utilisateur saisit une question en français
2. **Traitement Gemini** : L'API Gemini analyse et convertit en SQL
3. **Exécution SQL** : La requête SQL est exécutée sur la base SQLite
4. **Génération de réponse** : Une réponse naturelle est générée
5. **Retour à l'utilisateur** : Résultats + explication + confiance

## 🛡️ Sécurité

- Validation des requêtes SQL générées
- Protection contre l'injection SQL
- Limitation de la longueur des requêtes
- Seules les requêtes SELECT sont autorisées