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
    st.stop()

if not HF_TOKEN:
    st.warning("Veuillez ajouter votre token Hugging Face dans le fichier `.env`. Redémarrez l'application après avoir ajouté le token.")
    st.stop()


# Menu de navigation
with st.sidebar:
    page = option_menu(
        menu_title="Navigation",
        options=["Accueil", "Synthèse du CV", "Offre d'emploi", "Matching"],
        icons=["house", "file-earmark-text", "briefcase", "arrows"],
        default_index=0,
    )

    if "cv_filename" in st.session_state:
        cv_filename = st.session_state['cv_filename']
        st.sidebar.markdown(
            f"""
            <div style="background-color: lightblue; padding: 10px;">
            CV uploadé : {cv_filename}
            </div>
            """,
            unsafe_allow_html=True
        )
    


# Chargement des pages
if page == "Accueil":
    homepage()
elif page == "Synthèse du CV":
    st.title("Page CV")
elif page == "Offre d'emploi":
    st.title("Page Offre")
elif page == "Matching":
    st.title("Page Matching")
