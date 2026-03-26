import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# REMPLACE CECI par ton URL Webhook Discord (dans les paramètres de ton salon Discord)
DISCORD_WEBHOOK_URL = "TON_URL_WEBHOOK_ICI"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-name', methods=['POST'])
def submit():
    nom_gravure = request.form.get('nom')
    
    if nom_gravure:
        payload = {
            "embeds": [{
                "title": "🔨 Nouvelle commande de gravure",
                "description": f"Nom à inscrire sur le cuivre : **{nom_gravure}**",
                "color": 15105570 # Couleur orange
            }]
        }
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        return "<h1>Merci ! Ton nom a été transmis à l'équipe V.E.X.</h1>"
    
    return "Erreur : le champ était vide.", 400

if __name__ == '__main__':
    # Important pour Render : utiliser le port fourni par l'environnement
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
