from flask import Flask, request, jsonify, render_template
import networkx as nx
from ford_min import chemin_minimal
from ford_max import chemin_maximal  # Importer l'algorithme de Ford Max

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculer_chemin_min', methods=['POST'])
def calculer_chemin_min():
    data = request.get_json()
    G = nx.DiGraph()
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    source = data['source']
    target = data['target']
    chemin = chemin_minimal(G, source, target)
    return jsonify(chemin)

@app.route('/calculer_chemin_max', methods=['POST'])
def calculer_chemin_max():
    data = request.get_json()
    G = nx.DiGraph()
    for edge in data['edges']:
        G.add_edge(edge['source'], edge['target'], weight=edge['weight'])
    
    source = data['source']
    target = data['target']
    chemin = chemin_maximal(G, source, target)
    return jsonify(chemin)

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=8000)  # Exemple : vous pouvez spécifier le port ici
