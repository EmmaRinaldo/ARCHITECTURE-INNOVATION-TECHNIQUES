from flask import Flask, request, jsonify
from flask_cors import CORS  # Ajout de CORS
import openai
import googlemaps
import os
from dotenv import load_dotenv
from chatbot_restaurants import refine_query_with_chatgpt, get_restaurant_suggestions

# Charger les clés API
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
google_maps_api_key = os.getenv("GOOGLE_MAPS_API_KEY")

# Initialiser Flask
app = Flask(__name__)
CORS(app)  # Autoriser toutes les origines (frontend peut communiquer avec backend)

gmaps = googlemaps.Client(key=google_maps_api_key)

@app.route('/find_restaurants', methods=['POST'])
def find_restaurants():
    data = request.json
    type_repas = data.get("type_repas")
    localisation = data.get("localisation")

    if not type_repas or not localisation:
        return jsonify({"error": "Veuillez fournir un type de repas et une localisation."}), 400

    refined_query = refine_query_with_chatgpt(openai_api_key, type_repas, localisation)
    restaurants = get_restaurant_suggestions(gmaps, localisation, refined_query)

    return jsonify({"restaurants": restaurants})

if __name__ == "__main__":
    app.run(debug=True)
