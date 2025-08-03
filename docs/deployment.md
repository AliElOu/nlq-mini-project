# Guide de déploiement

## Prérequis

- Python 3.8+
- Clé API Google Gemini
- SQLite (inclus avec Python)

## Déploiement local

1. **Installation**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configuration**
   ```bash
   cp .env.example .env
   # Éditer .env avec votre clé API
   ```

3. **Initialisation de la base de données**
   ```bash
   python data/populate_db.py
   ```

4. **Démarrage**
   ```bash
   python main.py
   ```

## Déploiement en production

### Docker (Recommandé)

1. **Créer un Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   EXPOSE 8000

   CMD ["python", "main.py"]
   ```

2. **Build et run**
   ```bash
   docker build -t nlq-ecommerce .
   docker run -p 8000:8000 -e GEMINI_API_KEY=your_key nlq-ecommerce
   ```

### Serveur Linux

1. **Installation des dépendances système**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv
   ```

2. **Configuration de l'application**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Service systemd** (optionnel)
   ```ini
   [Unit]
   Description=NLQ E-commerce API
   After=network.target

   [Service]
   Type=simple
   User=www-data
   WorkingDirectory=/path/to/nlq-mini-project
   Environment=PATH=/path/to/nlq-mini-project/venv/bin
   ExecStart=/path/to/nlq-mini-project/venv/bin/python main.py
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

### Variables d'environnement de production

```bash
export GEMINI_API_KEY="your_production_key"
export DEBUG="False"
export HOST="0.0.0.0"
export PORT="8000"
export DATABASE_PATH="/data/ecommerce.db"
```

## Monitoring et logs

### Logs d'application

Ajouter la configuration de logging dans `config/settings.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Monitoring de santé

L'endpoint `/health` peut être utilisé pour les vérifications de santé.

### Métriques recommandées

- Temps de réponse des requêtes
- Taux d'erreur
- Utilisation de l'API Gemini
- Taille de la base de données

## Sécurité

### HTTPS

En production, utilisez toujours HTTPS avec un reverse proxy comme Nginx:

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Variables d'environnement sensibles

- Ne jamais commiter les clés API
- Utiliser des secrets managers en production
- Restreindre l'accès aux fichiers de configuration

## Sauvegarde

### Base de données

```bash
# Sauvegarde
cp database/ecommerce.db backup/ecommerce_$(date +%Y%m%d).db

# Restauration
cp backup/ecommerce_20240101.db database/ecommerce.db
```

### Automatisation

```bash
#!/bin/bash
# Cron job quotidien
0 2 * * * /path/to/backup_script.sh
```

## Troubleshooting

### Problèmes courants

1. **Erreur clé API Gemini**
   - Vérifier que la clé est correcte
   - Vérifier les quotas API

2. **Erreur de base de données**
   - Vérifier les permissions du fichier SQLite
   - Vérifier l'espace disque

3. **Performance lente**
   - Optimiser les requêtes SQL
   - Ajouter des index à la base de données
   - Implémenter un cache

### Logs utiles

```bash
# Voir les logs en temps réel
tail -f app.log

# Filtrer les erreurs
grep "ERROR" app.log

# Analyser les requêtes
grep "query" app.log | tail -20
```
