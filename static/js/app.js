/**
 * NLQ E-commerce - Script JavaScript simplifié
 */

// Variables globales
let currentRequest = null;

/**
 * Initialisation de l'application
 */
document.addEventListener('DOMContentLoaded', function () {
    console.log('🚀 NLQ E-commerce démarré');

    // Initialiser les événements
    initializeEvents();

    // Initialiser les suggestions
    initializeSuggestions();

    // Focus sur le champ de recherche
    document.getElementById('queryInput').focus();
});

/**
 * Initialise les événements
 */
function initializeEvents() {
    const queryInput = document.getElementById('queryInput');
    const searchButton = document.getElementById('searchButton');

    // Recherche avec Entrée
    queryInput.addEventListener('keypress', function (event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            executeQuery();
        }
    });

    // Validation de l'input
    queryInput.addEventListener('input', function () {
        const value = this.value.trim();
        searchButton.disabled = value.length === 0;

        // Limiter la longueur
        if (value.length > 500) {
            this.value = value.substring(0, 500);
        }
    });

    // Bouton de recherche
    searchButton.addEventListener('click', executeQuery);
}

/**
 * Initialise les suggestions
 */
function initializeSuggestions() {
    const suggestions = document.querySelectorAll('.suggestion');
    suggestions.forEach(suggestion => {
        suggestion.addEventListener('click', function () {
            const query = this.getAttribute('data-query');
            document.getElementById('queryInput').value = query;
            document.getElementById('searchButton').disabled = false;
            executeQuery();
        });
    });
}

/**
 * Exécute une requête
 */
async function executeQuery() {
    const queryInput = document.getElementById('queryInput');
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    const searchButton = document.getElementById('searchButton');

    const query = queryInput.value.trim();
    if (!query) {
        alert('Veuillez saisir une requête');
        return;
    }

    // Annuler la requête précédente
    if (currentRequest) {
        currentRequest.abort();
    }

    const controller = new AbortController();
    currentRequest = controller;

    try {
        // État de chargement
        searchButton.disabled = true;
        searchButton.innerHTML = '🔄 Recherche...';

        showLoading(resultsDiv, resultsContent);

        // Envoyer la requête
        const response = await fetch('/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query }),
            signal: controller.signal
        });

        if (!response.ok) {
            throw new Error(`Erreur ${response.status}: ${response.statusText}`);
        }

        const result = await response.json();

        // Afficher les résultats
        if (result.success) {
            displaySuccess(result, resultsContent);
        } else {
            displayError(result, resultsContent);
        }

    } catch (error) {
        if (error.name !== 'AbortError') {
            console.error('Erreur:', error);
            displayConnectionError(error, resultsContent);
        }
    } finally {
        // Réactiver le bouton
        searchButton.disabled = false;
        searchButton.innerHTML = '<span class="button-icon">🔍</span><span class="button-text">Rechercher</span>';
        currentRequest = null;
    }
}

/**
 * Affiche l'état de chargement
 */
function showLoading(resultsDiv, resultsContent) {
    resultsContent.innerHTML = `
        <div class="loading">
            <div class="loading-content">
                🔄 Analyse de votre requête en cours...
            </div>
        </div>
    `;
    resultsDiv.style.display = 'block';
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Formate le texte de réponse pour améliorer la lisibilité
 */
function formatResponseText(text) {
    if (!text) return 'Aucune réponse disponible';

    // Remplacer les astérisques par du HTML bold
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Traiter les listes avec puces
    text = text.replace(/\* \*\*(.*?)\*\*(.*?)(?=\n\*|\n[A-Z]|\n$|$)/g,
        '<div class="product-item"><strong class="product-category">$1</strong><span class="product-details">$2</span></div>');

    // Traiter les paragraphes
    text = text.replace(/\n\n/g, '</p><p>');
    text = '<p>' + text + '</p>';

    // Nettoyer les paragraphes vides
    text = text.replace(/<p><\/p>/g, '');

    // Traiter les prix avec mise en évidence
    text = text.replace(/(\d+[\.,]\d+€)/g, '<span class="price">$1</span>');

    // Traiter les prix barrés (au lieu de)
    text = text.replace(/\(au lieu de ([\d,\.]+€)\)/g, '<span class="old-price">(au lieu de $1)</span>');

    return text;
}

/**
 * Affiche les résultats de succès avec formatage amélioré
 */
function displaySuccess(result, container) {
    const confidence = Math.round((result.confidence || 0) * 100);
    const confidenceColor = getConfidenceColor(result.confidence || 0);
    const formattedResponse = formatResponseText(result.natural_response);

    container.innerHTML = `
        <div class="result-card success">
            <h3>✅ Résultats trouvés (${result.count || 0})</h3>
            
            <div class="response-text">
                <strong>🤖 Réponse :</strong>
                <div class="response-content formatted-content">${formattedResponse}</div>
            </div>
            
            <div class="stats-container">
                <div class="stat-item">🎯 Confiance : ${confidence}%</div>
                <div class="stat-item">📊 ${result.count || 0} résultat(s)</div>
            </div>
            
            <div class="confidence-container">
                <div class="confidence-bar">
                    <div class="confidence-fill" style="width: ${confidence}%; background: ${confidenceColor}"></div>
                </div>
            </div>
            
            <details>
                <summary>🔧 Détails techniques</summary>
                <div class="details-content">
                    <div class="technical-info">
                        <div class="info-section">
                            <strong>📝 Explication :</strong>
                            <p>${result.explanation || 'Non disponible'}</p>
                        </div>
                        <div class="info-section">
                            <strong>💾 Requête SQL :</strong>
                            <div class="sql-code">${result.sql_query || 'Non disponible'}</div>
                        </div>
                    </div>
                </div>
            </details>
        </div>
    `;
}/**
 * Affiche les erreurs
 */
function displayError(result, container) {
    container.innerHTML = `
        <div class="result-card error">
            <h3>❌ Erreur rencontrée</h3>
            <div class="response-text">
                <strong>📋 Message :</strong>
                <div class="error-content">
                    ${result && (result.natural_response || result.error) || 'Une erreur inattendue s\'est produite'}
                </div>
            </div>
            
            <div class="error-suggestions">
                <strong>💡 Suggestions :</strong>
                <ul>
                    <li>Vérifiez l'orthographe de votre requête</li>
                    <li>Essayez une formulation différente</li>
                    <li>Utilisez des termes plus simples</li>
                </ul>
            </div>
        </div>
    `;
}

/**
 * Affiche les erreurs de connexion
 */
function displayConnectionError(error, container) {
    container.innerHTML = `
        <div class="result-card error">
            <h3>Erreur</h3>
        </div>
    `;
}

/**
 * Détermine la couleur de confiance
 */
function getConfidenceColor(confidence) {
    if (confidence >= 0.8) return '#10b981';  // Vert
    if (confidence >= 0.6) return '#f59e0b';  // Orange
    return '#ef4444';  // Rouge
}

/**
 * Affiche un toast de notification
 */
function showToast(message, type = 'info') {
    // Créer ou récupérer le toast
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: 500;
            z-index: 1000;
            transform: translateX(400px);
            transition: transform 0.3s ease;
            max-width: 300px;
        `;
        document.body.appendChild(toast);
    }

    // Style selon le type
    const styles = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#2563eb'
    };

    toast.style.backgroundColor = styles[type] || styles.info;
    toast.textContent = message;

    // Afficher
    toast.style.transform = 'translateX(0)';

    // Masquer après 3 secondes
    setTimeout(() => {
        toast.style.transform = 'translateX(400px)';
    }, 3000);
}

// Export des fonctions principales
window.NLQApp = {
    executeQuery,
    showToast
};
