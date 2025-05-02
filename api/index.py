from flask import Flask, render_template, request, jsonify, json
import sys
import os

# Ajouter le répertoire parent au path pour pouvoir importer les fonctions
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importation des fonctions nécessaires
from app import find_combinations, generate_svg, elements, atomic_numbers, element_symbols

# Créer une application Flask spécifique pour Vercel
app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Ajouter un template filter pour une meilleure sérialisation JSON
@app.template_filter('tojson')
def tojson_filter(obj):
    return json.dumps(obj)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    name = ""
    svg = ""
    combinations = []
    
    if request.method == 'POST':
        name = request.form.get('name', '')
        combinations = find_combinations(name)
        
        if combinations:
            # Utiliser la première combinaison trouvée
            result = combinations[0]
            svg = generate_svg(result)
    
    return render_template('index.html', name=name, result=result, svg=svg, combinations=combinations)

@app.route('/download-svg', methods=['POST'])
def download_svg():
    try:
        data = request.get_json(force=True)
        symbols = data.get('symbols', []) if data else []
        
        # Vérifier que les symboles sont valides
        valid_symbols = [sym for sym in symbols if sym in elements]
        
        svg = generate_svg(valid_symbols)
        return jsonify({"svg": svg})
    except Exception as e:
        app.logger.error(f"Erreur lors du traitement de la requête: {str(e)}")
        return jsonify({"error": str(e), "svg": "<svg width='300' height='100'><text x='10' y='50' font-family='serif' font-size='16'>Erreur de traitement</text></svg>"}), 400

# Point d'entrée pour Vercel
handler = app 