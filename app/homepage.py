import os
import sys
import pandas as pd
import streamlit as st
import requests

def homepage():
    st.title("Bienvenue sur JobMatch")
    st.write("Cette application vous permet d'améliorer votre CV par rapport à une offre d'emploi")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("CV")
        st.write("Ajouter ici votre CV")
        uploaded_file = st.file_uploader("Choisir un fichier", type=['pdf'], accept_multiple_files=False)
        if uploaded_file is not None:
            cv_filename = uploaded_file.name
            st.success(f"'{cv_filename}' chargé avec succès")
    
    with col2:
        st.subheader("Offre d'emploi")
        url_offre = st.text_input("Insérer ici le lien de l'offre d'emploi")
        if url_offre:
            try:
                response = requests.get(url_offre)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur lors du chargement de l'offre d'emploi: {e}")
            else:
                st.success("L'URL de l'offre d'emploi est valide")
    
