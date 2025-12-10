from client_llamacpp import send_llama_chat



answer = send_llama_chat(system_prompt="""Tu dois déterminer si tu dispose des de toutes les informations nécessaires pour répondre à la question.
Si la question correspond à une demande de météo en fonction d'une ville et d'une date.
Tu analyses si tu as toutes les informations nécessaires (ville et date).
Tu réponds de la manière suivante:
```
{
    "has_date" : true or false,
    "has_city" : true or false
}
```                 
""",
                        user_content="""
                        Yo! il fait quel temps à Annecy?
                        """)

start = answer.find("```")
end = answer.find("```", start + 3)
if start != -1 and end != -1:
    current_state = answer[start + 3:end].strip()
else:
    current_state = answer.strip()
print("Current state extracted:\n", current_state)
# extract values from the json-like response 
import json
state_dict = json.loads(current_state)
has_date = state_dict.get("has_date", 0)
has_city = state_dict.get("has_city", 0)    
print(f"has_date: {has_date}, has_city: {has_city}")

# answer = send_llama_chat(system_prompt="""Si on te demande la météo pour une ville, tu réponds:
#                         ```get_weather("nom_de_la_ville", date)```
# Si tu as besoin de connaitre la date actuelle, tu réponds:
#                         ```get_current_date()```
                         
# Etapes à suivre:
# Soit il te manque des informations pour répondre à la question, soit tu disposes de toutes les informations nécessaires.
                         
# # CAS INFORMATIONS MANQUANTES:
#     1. Si la date actuelle est nécessaire, utilise get_current_date() pour l'obtenir.
#     2. Utilise la date obtenue pour formuler la requête météo avec get_weather("nom_de_la_ville", date).
# # CAS INFORMATIONS DISPONIBLES:
#     1. Fournis la réponse directement sans appeler de fonction.
                         
#                         """,
#                         user_content="""
#                         Yo! il fait quel temps à Annecy aujourd'hui?
#                         """)



# print(answer)
# # Extract the function call from the answer
# start = answer.find("```")
# end = answer.find("```", start + 3)
# if start != -1 and end != -1:
#     function_call = answer[start + 3:end].strip()
#     print("Function call extracted:", function_call)
