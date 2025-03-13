import os
import sys
import pandas as pd
import streamlit as st
import requests
from utils.ia import analyze_cv, analyze_offre_emploi , calculate_similarity
from utils.classFactory import ScrapingFactory


def offre_emploi_page():
    """
    Page centrale de l'application : l'utilisateur peut soit 
    - insérer l'URL d'une offre d'emploi pour la comparer à son CV
    - demande à l'application de suggérer des offre d'emploi pertinentes par rapport à son CV

    """

    col1, barre_verticale, col2 = st.columns([1, 0.05, 1])

    with col1:
        st.subheader("Comparer votre CV à une offre d'emploi qui vous intéresse")
        url_offre = st.text_input("Insérer ici le lien de l'offre d'emploi")
        st.session_state['url_offre'] = url_offre

        if url_offre:
            try:
                scraper = ScrapingFactory()
                brute = scraper.scrap_one(url_offre)
                @st.cache_data
                def get_offre(brute_description):
                    return analyze_offre_emploi(brute_description)

                offre = get_offre(brute['description'])
                st.write(offre)
                # response = requests.get(url_offre)
                # response.raise_for_status()
            except requests.exceptions.RequestException as e:
                st.error(f"Erreur lors du chargement de l'offre d'emploi: {e}")
            else:
                st.success("L'URL de l'offre d'emploi est valide")
        
            if 'cv_json' in st.session_state:
                cv_json = st.session_state['cv_json']
                @st.cache_data
                def get_similarity_score(cv_json, offre):
                    return calculate_similarity(cv_json, offre)

                score = get_similarity_score(cv_json, offre)
                st.write(f"Score de similarité: {score}")
                # st.write("")

    with barre_verticale:
        st.markdown("<div style='border-left: 10px solid gray; height: 100%;'></div>", unsafe_allow_html=True)

    with col2:
        st.subheader("Suggérer des offre d'emploi pertinentes")
        recherche_offre = st.button(label="Lancer la recherche")
        if recherche_offre:
            for i in range(1, 6):
                st.button(label=f"Offre_emploi_{i}")
