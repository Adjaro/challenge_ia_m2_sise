import os
import sys
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import find_dotenv, load_dotenv

# Importation des pages de l'application
from homepage import homepage
from components import show_sidebar, comparer_cv
from utils.ia import EnvironmentMetrics

# Initialiser le monitoring de l'environnement au démarrage
st.session_state["domaine_offre"] = False

# Vérifier si la session n'est pas déjà initialisée
if "monitoring_environnement" not in st.session_state:
    monitoring_environnement = EnvironmentMetrics()
    st.session_state["monitoring_environnement"] = monitoring_environnement

# Charger les variables d'environnement
load_dotenv(find_dotenv())
API_KEY = os.getenv("MISTRAL_API_KEY")
API_KEY = "7J4S9NaH3Fv7IU7lfTsqgzTfcpfS2pYw"
HF_TOKEN = os.getenv("HF_TOKEN")

if not API_KEY:
    st.warning(
        "Veuillez ajouter votre clé API Mistral dans le fichier `.env`. Redémarrez l'application après avoir ajouté la clé."
    )
    st.stop()

if not HF_TOKEN:
    st.warning(
        "Veuillez ajouter votre token Hugging Face dans le fichier `.env`. Redémarrez l'application après avoir ajouté le token."
    )
    st.stop()


# CSS personnalisé pour centrer la sidebar, arrondir les bordures, ajouter une couleur de fond et des marges
st.markdown(
    """
    <style>
        /* Centrer la sidebar */
        section[data-testid="stSidebar"] {
            top: 50% !important;
            transform: translateY(-50%) !important;
            height: 60% !important;
            border-radius: 20px !important; /* Arrondir les coins de la sidebar */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important; /* Ajouter une ombre */
            background-color: #f0f2f6 !important; /* Couleur de fond de la sidebar */
            margin-left: 20px !important; /* Marge à gauche */
            margin-right: 20px !important; /* Marge à droite */
            padding: 10px !important; /* Espacement interne */
        }

        /* Arrondir les bordures des boîtes dans la sidebar */
        .st-eb, .st-cb, .st-db, .st-fb {
            border-radius: 10px !important;
            padding: 10px !important;
            margin: 5px 0 !important;
           
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important; /* Ombre légère pour les boîtes */
        }

        /* Style pour les boutons dans la sidebar */
        .stButton > button {
            border-radius: 10px !important;
            padding: 10px 20px !important;
            font-size: 16px !important;
            transition: background-color 0.3s ease !important;
            background-color: #4CAF50 !important; /* Couleur de fond du bouton */
           
            border: none !important; /* Supprimer la bordure */
        }
 
        .stButton > button:hover {
            background-color: #615533 !important; /* Couleur de fond au survol */
        }

        /* Style pour les titres dans la sidebar */
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
            color: #615533 !important; /* Couleur du texte des titres */
        }
    </style>
""",
    unsafe_allow_html=True,
)


# Menu de navigation
# init_state()

if "uploaded_cv" not in st.session_state:
    homepage()
elif "uploaded_cv" in st.session_state and "url" not in st.session_state:
    cv_info = st.session_state["cv_json"]
    show_sidebar(cv_info)
    comparer_cv()
