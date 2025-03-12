import os
import sys
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from dotenv import find_dotenv, load_dotenv

# Importation des pages de l'application
from homepage import homepage

# Charger les variables d'environnement
load_dotenv(find_dotenv())
API_KEY = os.getenv("MISTRAL_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

if not API_KEY:
    st.warning("Veuillez ajouter votre clé API Mistral dans le fichier `.env`. Redémarrez l'application après avoir ajouté la clé.")
    return

if not HF_TOKEN:
    st.warning("Veuillez ajouter votre token Hugging Face dans le fichier `.env`. Redémarrez l'application après avoir ajouté le token.")
    return


# Menu de navigation
with st.sidebar:
    page = option_menu(
        menu_title="Navigation",
        options=["Accueil", "CV", "Offre", "Matching"],
        icons=["house", "plus-circle", "search", "arrow-left-right", "robot", "graph-up"],
        menu_icon="list",
        default_index=0,
    )

    if "cv_filename" in st.session_state:
        cv_filename = st.session_state['cv_filename']
        st.sidebar.markdown(
            f"""
            <div style="background-color: lightgreen; padding: 10px;">
            CV uploadé : {cv_filename}
            </div>
            """,
            unsafe_allow_html=True
        )
# Chargement des pages
if page == "Accueil":
    homepage()
elif page == "CV":
    st.title("Page CV")
elif page == "Offre":
    st.title("Page Offre")
elif page == "Matching":
    st.title("Page Matching")
