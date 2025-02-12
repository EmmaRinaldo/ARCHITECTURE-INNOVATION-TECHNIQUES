import openai
import googlemaps
import os
from dotenv import load_dotenv

def load_api_keys():
    load_dotenv()
    return os.getenv("OPENAI_API_KEY"), os.getenv("GOOGLE_MAPS_API_KEY")

def get_user_preferences():
    print("Bienvenue ! Je vais t'aider à choisir un restaurant.")
    type_repas = input("Que veux-tu manger ? (ex: pizza, sushi, vegan, créole, etc.) : ")
    localisation = input("Où cherches-tu un restaurant ? (ville ou adresse) : ")
    return type_repas, localisation

def refine_query_with_chatgpt(api_key, user_input, location):
    """
    Utilise ChatGPT pour reformuler la requête afin d'améliorer la recherche de restaurants pertinents,
    en intégrant des mots-clés optimisés pour Google Maps, en corrigeant les fautes d'orthographe,
    et en ajoutant le lieu pour plus de précision.
    """
    openai.api_key = api_key
    prompt = f"""
    Un utilisateur cherche un restaurant correspondant à sa demande : "{user_input}" dans la ville de "{location}".
    1. Corrige toute faute d'orthographe ou terme incorrect lié à la cuisine.
    2. Reformule cette demande en une requête optimisée sous forme de mots-clés pertinents pour un moteur de recherche comme Google Maps.
    3. Assure-toi d'inclure des termes précis liés à la spécialité et au type de cuisine recherchés.
    4. Donne uniquement la requête optimisée sans explication supplémentaire.
    """
    
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un assistant expert en recherche de restaurants."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content.strip()

def get_restaurant_suggestions(gmaps, location, query):
    geocode_result = gmaps.geocode(location)
    if not geocode_result:
        print("Erreur : Localisation introuvable.")
        return []
    
    lat, lng = geocode_result[0]['geometry']['location'].values()
    places_result = gmaps.places(query=query, location=(lat, lng), radius=1500, type='restaurant')
    
    restaurants = []
    for place in places_result.get("results", [])[:5]:
        name = place.get("name")
        address = place.get("formatted_address", "Adresse inconnue")
        place_id = place.get("place_id")
        phone = place.get("formatted_phone_number", "Non disponible")
        maps_url = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
        
        restaurants.append({
            "nom": name,
            "adresse": address,
            "téléphone": phone,
            "lien_map": maps_url
        })
    
    return restaurants

def main():
    openai_api_key, google_maps_api_key = load_api_keys()
    gmaps = googlemaps.Client(key=google_maps_api_key)
    
    type_repas, localisation = get_user_preferences()
    
    print("Optimisation de la requête avec ChatGPT...")
    refined_query = refine_query_with_chatgpt(openai_api_key, type_repas, localisation)
    
    print("Recherche des restaurants...")
    restaurants = get_restaurant_suggestions(gmaps, localisation, refined_query)
    
    if not restaurants:
        print("Désolé, aucun restaurant correspondant n'a été trouvé.")
        return
    
    print("Voici quelques suggestions :")
    for idx, resto in enumerate(restaurants, start=1):
        print(f"{idx}. {resto['nom']}")
        print(f"   📍 Adresse : {resto['adresse']}")
        print(f"   📞 Téléphone : {resto['téléphone']}")
        print(f"   🔗 Lien Google Maps : {resto['lien_map']}")
        print("------------------------------------")

if __name__ == "__main__":
    main()
