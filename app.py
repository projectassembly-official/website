import os
import requests
from flask import Flask, render_template, request
from datetime import datetime
import pytz

app = Flask(__name__)

# --- CONFIGURATION VIA LES VARIABLES D'ENVIRONNEMENT ---
WEBHOOKS = {
    "cuivre": os.environ.get("WEBHOOK_CUIVRE"),
    "bronze": os.environ.get("WEBHOOK_BRONZE"),
    "mix": os.environ.get("WEBHOOK_MIX")
}

def get_toronto_time():
    # Récupère l'heure actuelle précise au fuseau de l'Est
    tz = pytz.timezone('America/Toronto')
    return datetime.now(tz)

@app.route('/gravure/<type_metal>')
def index(type_metal):
    if type_metal not in ["cuivre", "bronze", "mix"]:
        return "Type de métal invalide", 404
    return render_template('index.html', metal=type_metal)

@app.route('/submit-name/<type_metal>', methods=['POST'])
def submit(type_metal):
    nom = request.form.get('nom')
    webhook_url = WEBHOOKS.get(type_metal)
    
    if not nom or not webhook_url:
        return "Erreur : Configuration manquante.", 400

    # Calcul de l'heure au moment du clic
    now = get_toronto_time()
    date_str = now.strftime("%Y, %m, %d")
    heure_str = now.strftime("%H, %M, %S")

    # Personnalisation selon le palier
    if type_metal == "cuivre":
        item, prix = "JETSON ORIN NANO SUPER!!!", "400"
        desc = f"**Cuivre**, avec **gravé {nom}**"
    elif type_metal == "bronze":
        item, prix = "JETSON AGX ORIN!!!", "2800"
        desc = f"**Bronze**, avec **gravé {nom}**"
    else:
        item, prix = "JETSON THOR!!!", "5000"
        desc = f"**Bronze, cuivre, tungstène et fibre de carbon**, avec **gravé {nom}**"

    # Construction du message EXACT que tu voulais
    message = (
        f"**Quelqu'un** vient de nous **acheter** un ***`{item}`*** Son **nom**: {nom}\n"
        f"Le **{date_str}** à **{heure_str}**\n\n"
        f"Ça lui a coûté **{prix}*$***\n\n"
        f"{desc}"
    )

    # Envoi à Discord
    requests.post(webhook_url, json={"content": message})
    
    return f"<h1>Merci {nom} ! Ton nom a été envoyé pour la gravure {type_metal}.</h1>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
