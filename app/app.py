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



# Sidebar
with st.sidebar:

    if "cv_filename" in st.session_state:
        cv_filename = st.session_state['cv_filename']
        st.sidebar.markdown(
            f"""
            <div style="background-color: blue; padding: 10px; word-wrap: break-word;">
            CV uploadé : <span style="font-size: smaller;">{cv_filename}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add space between the two markdowns

    if "url_offre" in st.session_state:
        url_offre = st.session_state['url_offre']
        st.sidebar.markdown(
            f"""
            <div style="background-color: green; padding: 10px; word-wrap: break-word;">
            URL de l'offre : <span style="font-size: smaller;">{url_offre}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    st.sidebar.markdown("<br>", unsafe_allow_html=True)  # Add space between the two markdowns

    if "cv_filename" in st.session_state :
        améliorer_cv = st.button("Améliorer mon CV")
    
    if "cv_filename" in st.session_state and "url_offre" in st.session_state:
        matching_cv_offre = st.button("Matching CV-offre d'emploi")
        
    

# Gestion de la navigation séquentielle
if "uploaded_cv" not in st.session_state :
    homepage()

elif "uploaded_cv" in st.session_state and "url" not in st.session_state:
    offre_emploi_page()

