import openai
import os
from dotenv import load_dotenv

# Charger la clé API depuis un fichier .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

def wicca_chatbot(prompt):
    client = openai.OpenAI()  # Nouvelle syntaxe avec un client OpenAI
    response = client.chat.completions.create(  # Nouvelle méthode
        model="gpt-4",  # Change en "gpt-3.5-turbo" si besoin
        messages=[
            {"role": "system", "content": "Tu es un expert en Wicca. Réponds aux questions des pratiquants avec des informations précises et bienveillantes."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content  # Accès correct à la réponse

if __name__ == "__main__":
    while True:
        user_input = input("\nPose ta question sur la Wicca (ou tape 'exit' pour quitter) : ")
        if user_input.lower() == "exit":
            break
        response = wicca_chatbot(user_input)
        print("\n🔮 Réponse :", response)
