import os
import sys
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu

# Importation des pages de l'application
from homepage import homepage



# Menu de navigation
with st.sidebar:
    page = option_menu(
        menu_title="Navigation",
        options=["Accueil", "CV", "Offre", "Matching"],
        icons=["house", "plus-circle", "search", "arrow-left-right", "robot", "graph-up"],
        menu_icon="list",
        default_index=0,
    )

    mistral_api_key = st.text_input("Entrez votre clef Mistral", type="password")
    hf_token = st.text_input("Entrez votre token Hugging Face", type="password")

    if mistral_api_key and hf_token:
        st.session_state['mistral_api_key'] = mistral_api_key
        st.session_state['hf_token'] = hf_token
        st.success("API key et token enregistrés")

# Chargement des pages
if page == "Accueil":
    homepage()
elif page == "CV":
    st.title("Page CV")
elif page == "Offre":
    st.title("Page Offre")
elif page == "Matching":
    st.title("Page Matching")
