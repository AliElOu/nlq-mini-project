"""
API FastAPI pour le système NLQ E-commerce
"""
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

# Configuration des fichiers statiques et templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

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
async def root(request: Request):
    """Page d'accueil avec interface moderne séparée"""
    return templates.TemplateResponse("index.html", {"request": request})

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
