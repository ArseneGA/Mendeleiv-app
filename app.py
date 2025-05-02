from flask import Flask, render_template, request, jsonify, json
import os

app = Flask(__name__)

# Dictionnaire des éléments chimiques avec leurs symboles et noms
elements = {
    "H": "Hydrogène", "He": "Hélium", "Li": "Lithium", "Be": "Béryllium", "B": "Bore", "C": "Carbone",
    "N": "Azote", "O": "Oxygène", "F": "Fluor", "Ne": "Néon", "Na": "Sodium", "Mg": "Magnésium",
    "Al": "Aluminium", "Si": "Silicium", "P": "Phosphore", "S": "Soufre", "Cl": "Chlore", "Ar": "Argon",
    "K": "Potassium", "Ca": "Calcium", "Sc": "Scandium", "Ti": "Titane", "V": "Vanadium", "Cr": "Chrome",
    "Mn": "Manganèse", "Fe": "Fer", "Co": "Cobalt", "Ni": "Nickel", "Cu": "Cuivre", "Zn": "Zinc",
    "Ga": "Gallium", "Ge": "Germanium", "As": "Arsenic", "Se": "Sélénium", "Br": "Brome", "Kr": "Krypton",
    "Rb": "Rubidium", "Sr": "Strontium", "Y": "Yttrium", "Zr": "Zirconium", "Nb": "Niobium", "Mo": "Molybdène",
    "Tc": "Technétium", "Ru": "Ruthénium", "Rh": "Rhodium", "Pd": "Palladium", "Ag": "Argent",
    "Cd": "Cadmium", "In": "Indium", "Sn": "Étain", "Sb": "Antimoine", "Te": "Tellure", "I": "Iode",
    "Xe": "Xénon", "Cs": "Césium", "Ba": "Baryum", "La": "Lanthane", "Ce": "Cérium", "Pr": "Praséodyme",
    "Nd": "Néodyme", "Pm": "Prométhium", "Sm": "Samarium", "Eu": "Europium", "Gd": "Gadolinium",
    "Tb": "Terbium", "Dy": "Dysprosium", "Ho": "Holmium", "Er": "Erbium", "Tm": "Thulium",
    "Yb": "Ytterbium", "Lu": "Lutécium", "Hf": "Hafnium", "Ta": "Tantale", "W": "Tungstène",
    "Re": "Rhénium", "Os": "Osmium", "Ir": "Iridium", "Pt": "Platine", "Au": "Or", "Hg": "Mercure",
    "Tl": "Thallium", "Pb": "Plomb", "Bi": "Bismuth", "Po": "Polonium", "At": "Astate", "Rn": "Radon",
    "Fr": "Francium", "Ra": "Radium", "Ac": "Actinium", "Th": "Thorium", "Pa": "Protactinium",
    "U": "Uranium", "Np": "Neptunium", "Pu": "Plutonium", "Am": "Américium", "Cm": "Curium",
    "Bk": "Berkélium", "Cf": "Californium", "Es": "Einsteinium", "Fm": "Fermium", "Md": "Mendélévium",
    "No": "Nobélium", "Lr": "Lawrencium", "Rf": "Rutherfordium", "Db": "Dubnium", "Sg": "Seaborgium",
    "Bh": "Bohrium", "Hs": "Hassium", "Mt": "Meitnérium", "Ds": "Darmstadtium", "Rg": "Roentgenium",
    "Cn": "Copernicium", "Nh": "Nihonium", "Fl": "Flérovium", "Mc": "Moscovium", "Lv": "Livermorium",
    "Ts": "Tennesse", "Og": "Oganesson",
    # Élément spécial pour les espaces
    "□": "Espace"
}

# Dictionnaire des catégories d'éléments pour les couleurs
element_categories = {
    # Métaux alcalins
    "Li": "alkali", "Na": "alkali", "K": "alkali", "Rb": "alkali", "Cs": "alkali", "Fr": "alkali",
    # Métaux alcalino-terreux
    "Be": "alkaline", "Mg": "alkaline", "Ca": "alkaline", "Sr": "alkaline", "Ba": "alkaline", "Ra": "alkaline",
    # Métaux de transition
    "Sc": "transition", "Ti": "transition", "V": "transition", "Cr": "transition", "Mn": "transition", 
    "Fe": "transition", "Co": "transition", "Ni": "transition", "Cu": "transition", "Zn": "transition",
    "Y": "transition", "Zr": "transition", "Nb": "transition", "Mo": "transition", "Tc": "transition", 
    "Ru": "transition", "Rh": "transition", "Pd": "transition", "Ag": "transition", "Cd": "transition",
    "Hf": "transition", "Ta": "transition", "W": "transition", "Re": "transition", "Os": "transition", 
    "Ir": "transition", "Pt": "transition", "Au": "transition", "Hg": "transition",
    # Lanthanides
    "La": "lanthanide", "Ce": "lanthanide", "Pr": "lanthanide", "Nd": "lanthanide", "Pm": "lanthanide", 
    "Sm": "lanthanide", "Eu": "lanthanide", "Gd": "lanthanide", "Tb": "lanthanide", "Dy": "lanthanide", 
    "Ho": "lanthanide", "Er": "lanthanide", "Tm": "lanthanide", "Yb": "lanthanide", "Lu": "lanthanide",
    # Actinides
    "Ac": "actinide", "Th": "actinide", "Pa": "actinide", "U": "actinide", "Np": "actinide", 
    "Pu": "actinide", "Am": "actinide", "Cm": "actinide", "Bk": "actinide", "Cf": "actinide", 
    "Es": "actinide", "Fm": "actinide", "Md": "actinide", "No": "actinide", "Lr": "actinide",
    # Métalloïdes
    "B": "metalloid", "Si": "metalloid", "Ge": "metalloid", "As": "metalloid", "Sb": "metalloid", "Te": "metalloid", "Po": "metalloid",
    # Non-métaux
    "H": "nonmetal", "C": "nonmetal", "N": "nonmetal", "O": "nonmetal", "P": "nonmetal", "S": "nonmetal", "Se": "nonmetal",
    # Halogènes
    "F": "halogen", "Cl": "halogen", "Br": "halogen", "I": "halogen", "At": "halogen", "Ts": "halogen",
    # Gaz nobles
    "He": "noble", "Ne": "noble", "Ar": "noble", "Kr": "noble", "Xe": "noble", "Rn": "noble", "Og": "noble",
    # Autres métaux
    "Al": "other-metal", "Ga": "other-metal", "In": "other-metal", "Sn": "other-metal", "Tl": "other-metal", "Pb": "other-metal", "Bi": "other-metal",
    # Éléments restants
    "□": "space"
}

# Dictionnaire des numéros atomiques
atomic_numbers = {
    "H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8, "F": 9, "Ne": 10,
    "Na": 11, "Mg": 12, "Al": 13, "Si": 14, "P": 15, "S": 16, "Cl": 17, "Ar": 18, "K": 19, "Ca": 20,
    "Sc": 21, "Ti": 22, "V": 23, "Cr": 24, "Mn": 25, "Fe": 26, "Co": 27, "Ni": 28, "Cu": 29, "Zn": 30,
    "Ga": 31, "Ge": 32, "As": 33, "Se": 34, "Br": 35, "Kr": 36, "Rb": 37, "Sr": 38, "Y": 39, "Zr": 40,
    "Nb": 41, "Mo": 42, "Tc": 43, "Ru": 44, "Rh": 45, "Pd": 46, "Ag": 47, "Cd": 48, "In": 49, "Sn": 50,
    "Sb": 51, "Te": 52, "I": 53, "Xe": 54, "Cs": 55, "Ba": 56, "La": 57, "Ce": 58, "Pr": 59, "Nd": 60,
    "Pm": 61, "Sm": 62, "Eu": 63, "Gd": 64, "Tb": 65, "Dy": 66, "Ho": 67, "Er": 68, "Tm": 69, "Yb": 70,
    "Lu": 71, "Hf": 72, "Ta": 73, "W": 74, "Re": 75, "Os": 76, "Ir": 77, "Pt": 78, "Au": 79, "Hg": 80,
    "Tl": 81, "Pb": 82, "Bi": 83, "Po": 84, "At": 85, "Rn": 86, "Fr": 87, "Ra": 88, "Ac": 89, "Th": 90,
    "Pa": 91, "U": 92, "Np": 93, "Pu": 94, "Am": 95, "Cm": 96, "Bk": 97, "Cf": 98, "Es": 99, "Fm": 100,
    "Md": 101, "No": 102, "Lr": 103, "Rf": 104, "Db": 105, "Sg": 106, "Bh": 107, "Hs": 108, "Mt": 109,
    "Ds": 110, "Rg": 111, "Cn": 112, "Nh": 113, "Fl": 114, "Mc": 115, "Lv": 116, "Ts": 117, "Og": 118,
    # Élément spécial pour les espaces (numéro fictif)
    "□": 0
}

# Conversion du dictionnaire pour la recherche insensible à la casse
element_symbols = {sym.lower(): sym for sym in elements.keys()}
# Ajout de l'espace comme élément spécial
element_symbols[' '] = '□'

# Ajout d'un template filter pour une meilleure sérialisation JSON
@app.template_filter('tojson')
def tojson_filter(obj):
    return json.dumps(obj)

def find_combinations(word):
    """Trouve toutes les combinaisons possibles d'éléments chimiques dans un mot."""
    word = word.lower()
    memo = {}

    def backtrack(index):
        if index == len(word):
            return [[]]
        if index in memo:
            return memo[index]

        combinations = []

        # Traitement spécial pour l'espace
        if word[index] == ' ':
            for suffix in backtrack(index + 1):
                combinations.append(['□'] + suffix)
        else:
            # Essai avec des symboles d'une ou deux lettres
            for length in [1, 2]:
                if index + length <= len(word):
                    part = word[index:index + length]
                    # Vérification qu'il n'y a pas d'espace dans la partie traitée
                    if ' ' not in part and part in element_symbols:
                        for suffix in backtrack(index + length):
                            combinations.append([element_symbols[part]] + suffix)

        memo[index] = combinations
        return combinations

    return backtrack(0)

def generate_svg(symbols):
    """Génère un SVG à partir d'une liste de symboles chimiques."""
    if not symbols:
        return """<svg width='300' height='120' xmlns="http://www.w3.org/2000/svg">
            <rect width="300" height="120" rx="8" fill="white" stroke="#000" stroke-width="1" />
            <text x='150' y='60' font-family='Inter, sans-serif' font-size='16' fill='#171717' text-anchor="middle">
                Aucune combinaison trouvée
            </text>
        </svg>"""
    
    # Configuration minimaliste noir et blanc pour le SVG
    box_width = 110
    box_height = 130
    margin = 12
    total_width = (box_width + margin) * len(symbols) - margin + 20  # Ajouter un peu d'espace à droite
    
    # Garantir une largeur minimale mais permettre l'expansion si nécessaire
    svg_width = max(total_width, 300)
    svg_height = box_height + 20
    
    # Définir le style CSS en noir et blanc 
    svg_style = """
    <style>
        .element-box { 
            fill: white; 
            stroke: #000; 
            stroke-width: 1.5;
            rx: 4;
            ry: 4; 
        }
        .element-symbol { 
            font-family: 'Inter', sans-serif; 
            font-size: 38px; 
            font-weight: 300; 
            text-anchor: middle;
            fill: #000;
        }
        .element-number { 
            font-family: 'Inter', sans-serif; 
            font-size: 12px; 
            font-weight: 500;
            text-anchor: start;
            fill: #404040;
        }
        .element-name { 
            font-family: 'Inter', sans-serif; 
            font-size: 12px; 
            font-weight: 400;
            text-anchor: middle;
            fill: #404040;
        }
        .decoration { 
            fill: none; 
            stroke: #e5e5e5; 
            stroke-width: 1;
        }
        .space-element { 
            fill: white;
            stroke: #d4d4d4; 
            stroke-dasharray: 2,2; 
            stroke-width: 1;
        }
    </style>
    """
    
    # SVG simplifié avec valeurs explicites pour garantir la compatibilité de défilement
    svg = f"""<svg width="{total_width}" height="{svg_height}" viewBox="0 0 {total_width} {svg_height}" xmlns="http://www.w3.org/2000/svg">
    {svg_style}
    """
    
    # Définir un léger padding à gauche
    start_x = 10
    
    for i, symbol in enumerate(symbols):
        x = start_x + i * (box_width + margin)
        y = 10
        
        # Déterminer la classe CSS
        element_class = "element-box"
        if symbol == "□":
            element_class += " space-element"
        
        # Rectangle principal
        svg += f"""<rect class="{element_class}" x="{x}" y="{y}" width="{box_width}" height="{box_height}" />"""
        
        # Décorations (lignes concentriques) sauf pour l'espace
        if symbol != "□":
            svg += f"""<rect class="decoration" x="{x+8}" y="{y+8}" width="{box_width-16}" height="{box_height-16}" rx="2" ry="2" />"""
        
        # Numéro atomique
        atomic_number = atomic_numbers.get(symbol, "?")
        svg += f"""<text class="element-number" x="{x+12}" y="{y+25}">{atomic_number}</text>"""
        
        # Symbole de l'élément
        svg += f"""<text class="element-symbol" x="{x+box_width/2}" y="{y+75}">{symbol}</text>"""
        
        # Nom de l'élément
        element_name = elements.get(symbol, "Inconnu")
        svg += f"""<text class="element-name" x="{x+box_width/2}" y="{y+box_height-15}">{element_name}</text>"""
    
    svg += "</svg>"
    return svg

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

if __name__ == '__main__':
    # Détecter si on est en production (variable d'environnement définie par les hébergeurs)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 