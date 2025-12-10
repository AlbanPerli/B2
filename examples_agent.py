
# =========================
# Handlers d'exemple
# =========================

from typing import Any, Dict

from agent import MultiSkillAgent, Skill, Slot

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from sound_file import AudioPlayer



def weather_on_ready(values: Dict[str, str]) -> Dict[str, Any]:
    city = values.get("city")
    date = values.get("date")

    return {
        "type": "weather_result",
        "city": city,
        "date": date,
        "forecast": {
            "summary": "ensoleillé avec quelques nuages",
            "temperature_min": 5,
            "temperature_max": 14,
        },
        "note": "Les données météo sont fictives dans cet exemple.",
    }

def booking_on_ready(values: Dict[str, str]) -> str:
    restaurant = values.get("restaurant_name", "un restaurant")
    date = values.get("date", "une date inconnue")
    time = values.get("time", "une heure inconnue")
    people = values.get("people", "un certain nombre de")

    return (
        f"Parfait ! Je récapitule : réservation à {restaurant}, "
        f"le {date} à {time}, pour {people} personnes. "
        f"(Je ne fais pas la réservation réelle, c'est un exemple.)"
    )

def audio_on_ready(values: Dict[str, str]) -> str:
    file = values.get("file_path", "un fichier")

    player = AudioPlayer(file)
    player.play()


def write_txt_file_on_ready(values: Dict[str, str]) -> str:
    file = values.get("file_path", "un fichier")
    content = values.get("content", "")
    with open(file, "w") as f:
        f.write(content)
    return f"Le contenu a été écrit dans le fichier {file}."


def read_txt_file_on_ready(values: Dict[str, str]) -> str:
    file = values.get("file_path", "un fichier")
    try:
        with open(file, "r") as f:
            content = f.read()
        return f"Contenu du fichier {file}:\n{content}"
    except FileNotFoundError:
        return f"Le fichier {file} n'existe pas."




# =========================
# Construction de l'agent
# =========================

def build_agent() -> MultiSkillAgent:
    # Skill météo
    weather_slots = [
        Slot(
            name="city",
            description="la ville pour la météo (ex: Annecy, Paris, Lyon)",
            question="Pour quelle ville veux-tu la météo ?",
        ),
        Slot(
            name="date",
            description="la date pour la météo (ex: aujourd'hui, demain, 2025-12-15)",
            question="Pour quelle date veux-tu la météo ?",
        ),
    ]

    weather_skill = Skill(
        name="weather",
        description="questions à propos de la météo en fonction d'une ville et d'une date",
        slots=weather_slots,
        final_answer_system_prompt="""Tu es un assistant météo. Tu reçois des données structurées (ville, date, prévisions, etc.) et tu dois formuler une réponse météo en français, concise et naturelle.""",
        on_ready=weather_on_ready,
    )

    # Skill réservation de restaurant
    booking_slots = [
        Slot(
            name="restaurant_name",
            description="le nom du restaurant ou type de cuisine (ex: italien, japonais)",
            question="Dans quel restaurant ou quel type de cuisine veux-tu réserver ?",
        ),
        Slot(
            name="date",
            description="la date de la réservation",
            question="Pour quel jour veux-tu réserver ?",
        ),
        Slot(
            name="time",
            description="l'heure de la réservation",
            question="À quelle heure ?",
        ),
        Slot(
            name="people",
            description="le nombre de personnes",
            question="Pour combien de personnes ?",
        ),
    ]

    booking_skill = Skill(
        name="booking",
        description="organisation d'une réservation de restaurant",
        slots=booking_slots,
        final_answer_system_prompt="""Tu es un assistant qui aide à réserver un restaurant. Tu reçois soit des données structurées, soit un résumé, et tu dois répondre en français en récapitulant clairement la réservation.""",
        on_ready=booking_on_ready,
    )

    # Skill smalltalk (pas de slots)
    smalltalk_skill = Skill(
        name="smalltalk",
        description="conversation générale, questions diverses, discuter de tout et de rien mais jamais des autres skills",
        slots=[],
        final_answer_system_prompt="""Tu es un assistant conversationnel général. Réponds naturellement en français, de façon sympathique et concise.""",
        on_ready=None,
    )

    # Skill audio
    audio_skill = Skill(
        name="play_audio_file",
        description="jouer un fichier audio, jouer de la musique",
        slots=[
            Slot(
                name="file_path",
                description="le chemin du fichier audio",
                question="Quel fichier audio veux-tu jouer ?",
            )
        ],
        final_answer_system_prompt="""Tu es un assistant qui permet d'écouter de la musique. Tu dois exécuter la lecture du fichier audio spécifié en fonction du chemin fourni.""",
        on_ready=audio_on_ready,
    )

    # Skill audio
    file_writer = Skill(
        name="write_txt_file",
        description="Ecrire du contenu dans un fichier texte",
        slots=[
            Slot(
                name="file_path",
                description="le chemin du fichier texte",
                question="Quel est le nom du fichier texte où écrire ?",
            ),
            Slot(
                name="content",
                description="le contenu du fichier texte",
                question="Quel est le contenu du fichier texte ?",
            )
        ],
        final_answer_system_prompt="""Tu es un assistant qui permet d'écrire du contenu dans un fichier texte. Tu dois créer ou écraser le fichier texte spécifié avec le contenu fourni.""",
        on_ready=write_txt_file_on_ready,
    )

    file_reader = Skill(
        name="read_txt_file",
        description="Lire du contenu dans un fichier texte",
        slots=[
            Slot(
                name="file_path",
                description="le chemin du fichier texte",
                question="Quel est le nom du fichier texte à lire ?",
            ),
        ],
        final_answer_system_prompt="""Tu es un assistant qui permet de lire du contenu dans un fichier texte. Tu dois lire le fichier texte spécifié et retourner son contenu.""",
        on_ready=read_txt_file_on_ready,
    )

    return MultiSkillAgent([
        weather_skill,
        booking_skill,
        audio_skill,
        file_writer,
        file_reader,
        smalltalk_skill
    ])

# =========================
# Boucle principale
# =========================

def main():
    agent = build_agent()
    print("Assistant: Salut !")
    print("Tu peux me parler météo, réservation de resto, ou juste discuter.")
    print("Tape 'quit' pour arrêter, ou 'reset' pour annuler une demande en cours.\n")

    while True:
        user_msg = input("Utilisateur: ").strip()
        if not user_msg:
            continue
        if user_msg.lower() in {"quit", "exit"}:
            print("Assistant: À bientôt !")
            break

        try:
            answer = agent.handle_user_message(user_msg)
        except Exception as e:
            print("Erreur interne:", e)
            answer = "Oups, j'ai eu un souci interne, peux-tu réessayer ?"

        print("Assistant:", answer)


if __name__ == "__main__":
    main()