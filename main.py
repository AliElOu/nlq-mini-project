"""
API FastAPI pour le système NLQ E-commerce
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import uvicorn

from src.nlq_service import NLQService
from config.settings import Config

# Initialisation de l'application FastAPI
app = FastAPI(
    title="NLQ E-commerce API",
    description="API pour les requêtes en langage naturel sur une base de données e-commerce",
    version="1.0.0"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialisation du service NLQ (sera fait à la demande)
nlq_service = None

def get_nlq_service():
    """Obtenir une instance du service NLQ avec gestion d'erreur"""
    global nlq_service
    if nlq_service is None:
        try:
            nlq_service = NLQService()
        except Exception as e:
            raise HTTPException(
                status_code=503, 
                detail=f"Service NLQ non disponible: {str(e)}. Vérifiez la configuration (clé API Gemini, etc.)"
            )
    return nlq_service

# Modèles Pydantic
class QueryRequest(BaseModel):
    query: str
    limit: Optional[int] = 10

class QueryResponse(BaseModel):
    success: bool
    data: List[Dict[str, Any]]
    sql_query: Optional[str] = None
    explanation: Optional[str] = None
    filters_applied: Optional[List[str]] = None
    confidence: Optional[float] = None
    natural_response: str
    count: int
    error: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def root():
    """Page d'accueil avec interface simple"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>NLQ E-commerce</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; }
            .query-form { margin: 20px 0; }
            input[type="text"] { width: 70%; padding: 10px; font-size: 16px; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; font-size: 16px; background: #007bff; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #0056b3; }
            .suggestions { margin: 20px 0; }
            .suggestion { background: #e9ecef; padding: 8px 12px; margin: 5px; border-radius: 15px; display: inline-block; cursor: pointer; }
            .suggestion:hover { background: #dee2e6; }
            .results { margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 5px; }
            .error { color: #dc3545; }
            .success { color: #28a745; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🛍️ NLQ E-commerce</h1>
            <p>Posez vos questions en langage naturel sur notre catalogue de vêtements !</p>
            
            <div class="query-form">
                <input type="text" id="queryInput" placeholder="Ex: Montre-moi tous les t-shirts pour homme en coton">
                <button onclick="executeQuery()">Rechercher</button>
            </div>
            
            <div class="suggestions">
                <strong>Suggestions :</strong><br>
                <span class="suggestion" onclick="setQuery('Montre-moi tous les t-shirts pour homme en coton')">T-shirts homme en coton</span>
                <span class="suggestion" onclick="setQuery('Quels sont les produits en promotion?')">Produits en promotion</span>
                <span class="suggestion" onclick="setQuery('Trouve des robes d\\'été de moins de 50 euros')">Robes d'été < 50€</span>
                <span class="suggestion" onclick="setQuery('Affiche les produits Nike disponibles')">Produits Nike</span>
            </div>
            
            <div id="results" class="results" style="display: none;">
                <div id="resultsContent"></div>
            </div>
        </div>
        
        <script>
            function setQuery(query) {
                document.getElementById('queryInput').value = query;
            }
            
            async function executeQuery() {
                const query = document.getElementById('queryInput').value;
                if (!query.trim()) {
                    alert('Veuillez saisir une requête');
                    return;
                }
                
                const resultsDiv = document.getElementById('results');
                const resultsContent = document.getElementById('resultsContent');
                
                resultsContent.innerHTML = '<p>Traitement en cours...</p>';
                resultsDiv.style.display = 'block';
                
                try {
                    const response = await fetch('/query', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ query: query })
                    });
                    
                    const result = await response.json();
                    
                    if (result.success) {
                        resultsContent.innerHTML = `
                            <div class="success">
                                <h3>Résultats (${result.count} trouvé(s))</h3>
                                <p><strong>Réponse :</strong> ${result.natural_response}</p>
                                <p><strong>Confiance :</strong> ${(result.confidence * 100).toFixed(1)}%</p>
                                <details>
                                    <summary>Détails techniques</summary>
                                    <p><strong>Requête SQL :</strong> <code>${result.sql_query}</code></p>
                                    <p><strong>Explication :</strong> ${result.explanation}</p>
                                </details>
                            </div>
                        `;
                    } else {
                        resultsContent.innerHTML = `
                            <div class="error">
                                <h3>Erreur</h3>
                                <p>${result.natural_response}</p>
                            </div>
                        `;
                    }
                } catch (error) {
                    resultsContent.innerHTML = `
                        <div class="error">
                            <h3>Erreur de connexion</h3>
                            <p>Impossible de traiter la requête : ${error.message}</p>
                        </div>
                    `;
                }
            }
            
            // Permettre l'exécution avec la touche Entrée
            document.getElementById('queryInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    executeQuery();
                }
            });
        </script>
    </body>
    </html>
    """
    return html_content

@app.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest):
    """
    Traiter une requête en langage naturel
    """
    try:
        service = get_nlq_service()
        result = service.process_query(request.query)
        return QueryResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")

@app.get("/suggestions")
async def get_suggestions():
    """Obtenir des suggestions de requêtes"""
    try:
        service = get_nlq_service()
        return {"suggestions": service.get_suggestions()}
    except HTTPException:
        raise
    except Exception as e:
        return {"suggestions": [
            "Montre-moi tous les produits",
            "Affiche les t-shirts",
            "Quels sont les prix?"
        ]}

@app.get("/stats")
async def get_database_stats():
    """Obtenir des statistiques sur la base de données"""
    try:
        service = get_nlq_service()
        return service.get_database_stats()
    except HTTPException:
        raise
    except Exception as e:
        return {"error": f"Impossible d'obtenir les statistiques: {str(e)}"}

@app.get("/health")
async def health_check():
    """Vérification de santé de l'API"""
    return {"status": "OK", "message": "NLQ E-commerce API is running"}

if __name__ == "__main__":
    # Valider la configuration avant de démarrer
    try:
        Config.validate()
        print("Configuration validée avec succès")
    except ValueError as e:
        print(f"Erreur de configuration: {e}")
        exit(1)
    
    # Démarrer le serveur
    uvicorn.run(
        "main:app",
        host=Config.HOST,
        port=Config.PORT,
        reload=Config.DEBUG
    )
