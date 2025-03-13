import os
import sys
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import find_dotenv, load_dotenv

# Importation des pages de l'application
from homepage import homepage
from componentsAlexis import offre_emploi_page


# Charger les variables d'environnement
load_dotenv(find_dotenv())
API_KEY = os.getenv("MISTRAL_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

if not API_KEY:
    st.warning("Veuillez ajouter votre clé API Mistral dans le fichier `.env`. Redémarrez l'application après avoir ajouté la clé.")
    st.stop()

if not HF_TOKEN:
    st.warning("Veuillez ajouter votre token Hugging Face dans le fichier `.env`. Redémarrez l'application après avoir ajouté le token.")
    st.stop()
 



# # Sidebar
# with st.sidebar:

#     if "cv_filename" in st.session_state:
#         cv_filename = st.session_state['cv_filename']
#         st.sidebar.markdown(
#             f"""
#             <div style="background-color: blue; padding: 10px; word-wrap: break-word;">
#             CV uploadé : <span style="font-size: smaller;">{cv_filename}</span>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )
    
#     st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add space between the two markdowns

#     if "url_offre" in st.session_state:
#         url_offre = st.session_state['url_offre']
#         st.sidebar.markdown(
#             f"""
#             <div style="background-color: green; padding: 10px; word-wrap: break-word;">
#             URL de l'offre : <span style="font-size: smaller;">{url_offre}</span>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )
    
#     st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add space between the two markdowns

#     if "cv_filename" in st.session_state :
#         améliorer_cv = st.button("Améliorer mon CV")
    
#     if "cv_filename" in st.session_state and "url_offre" in st.session_state:
#         matching_cv_offre = st.button("Matching CV-offre d'emploi")
        
    

# Gestion de la navigation séquentielle
if "uploaded_cv" not in st.session_state :
    homepage()
elif "uploaded_cv" in st.session_state and "url" not in st.session_state:
    offre_emploi_page()




# Exemple de données CV
cv_info = {
    "Profil": {
        "titre": "Data Scientist",
        "disponibilite": "Disponible immédiatement"
    },
    "Formation": [
        {
            "niveau_etudes": "Master",
            "domaine_etudes": ["Informatique", "Mathématiques appliquées"]
        }
    ],
    "Competences": [
        "Python", "SQL", "Terraform", "Bitbucket", "Jenkins", "Airflow", "Docker", 
        "Kubernetes", "GCP (BigQuery, Spark DataProc)", "Développement logiciel agile", 
        "Algorithmes d'apprentissage statistique"
    ],
    "Experiences": [
        {
            "domaine_activite": ["Data Science"],
            "poste_occupe": "Data Scientist",
            "duree": "5 ans"
        }
    ]
}

# Affichage de la barre latérale
# show_sidebar(cv_info)


# st.session_state['uploaded_cv'] = True
# if st.session_state.get('uploaded_cv') is not None:
#     # cv_info = show_sidebar()
#     show_sidebar(cv_info)


# if cv_info:
#     st.session_state['cv_info'] = cv_info
#     st.write(cv_info)



# Affichage de la barre latérale
# SELECTED_CHAT = show_sidebar()

# # Stockage du chat sélectionné
# if SELECTED_CHAT:
#     st.session_state["selected_chat"] = SELECTED_CHAT
# elif "selected_chat" not in st.session_state and SELECTED_CHAT:
#     st.session_state["selected_chat"] = SELECTED_CHAT

# # Affichage du chat sélectionné
# if (
#     "selected_chat" in st.session_state
#     and st.session_state["selected_chat"] is not None
# ):
#     current_chat = st.session_state["selected_chat"]
#     st.subheader(f"{current_chat}")

#     # Initialisation de l'historique des messages pour le chat sélectionné
#     if current_chat not in st.session_state["chats"]:
#         st.session_state["chats"][current_chat] = []

#     # Création de l'instance du chat
#     initial_question = st.session_state.get("initial_question", None)
#     chat = Chat(selected_chat=current_chat, initial_question=initial_question)

#     # Affichage du chat sélectionné
#     chat.run()

#     # Sauvegarde des messages du chat sélectionné
#     st.session_state["chats"][current_chat] = st.session_state.get("chats", {}).get(
#         current_chat, []
#     )
# else:
#     st.container(height=200, border=False)
#     with st.container():
#         # Affichage si une ou plusieurs clés d'API sont introuvables
#         if st.session_state["found_api_keys"] is False:
#             # Titre
#             st.title("Je ne peux pas vous aider... 😢")

#             # Message d'erreur
#             st.error(
#                 "**Conversation avec l'IA indisponible :** "
#                 "Une ou plusieurs clés d'API sont introuvables.",
#                 icon=":material/error:",
#             )
#         else:
#             if len(st.session_state["chats"]) < 5:
#                 # Titre
#                 st.title("Comment puis-je vous aider ? 🤩")

#                 # Barre de saisie de question
#                 question = st.chat_input("Écrivez votre message", key="new_chat_question")

#                 if question:
#                     st.session_state["initial_question"] = question
#                     create_new_chat()
#                     st.rerun()

#                 # Génération de questions suggérées
#                 if "suggested_questions" not in st.session_state:
#                     chat_instance = Chat(selected_chat="suggestions")
#                     st.session_state["suggested_questions"] = (
#                         chat_instance.get_suggested_questions()
#                     )

#                 # Suggestions de questions dynamiques
#                 suggestions = st.pills(
#                     label=(
#                         "Sinon voici quelques suggestions de questions que j'ai générées "
#                         "et que vous pouvez me poser :"
#                     ),
#                     options=st.session_state["suggested_questions"]
#                 )

#                 if suggestions:
#                     st.session_state["initial_question"] = suggestions
#                     create_new_chat()
#                     st.rerun()
#             else:
#                 # Titre
#                 st.title("Limite de conversations atteinte 🤯")

#                 # Message d'information
#                 st.info(
#                     "Nombre maximal de conversations atteint, "
#                     "supprimez-en une pour en commencer une nouvelle",
#                     icon=":material/feedback:",
#                 )