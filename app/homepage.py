import os
import sys
import pandas as pd
import streamlit as st

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
        st.write("Insérer ici le lien de l'offre d'emploi")
        url_offre = st.text_input("Lien de l'offre d'emploi")
        if url_offre:
            st.success("Offre d'emploi chargée avec succès")
    
