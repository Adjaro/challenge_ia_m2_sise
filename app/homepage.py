import os
import sys
import pandas as pd
import streamlit as st
import requests
from utils.ia import read_pdf, analyze_cv, analyze_cv_offre_emploi , calculate_similarity
from utils.classFactory import ScrapingFactory

def homepage():
    """
    Première page de l'application : 
    l'utilisateur doit y charger un CV au format PDF 
    avant d'utiliser les autres fonctionnalités
    """
    
    st.title("Bienvenue sur JobMatch")
    st.write("Cette application vous permet d'améliorer votre candidature par rapport à des offres d'emplois qui vous intéresse")

    uploaded_cv = st.file_uploader(label="Pour commencer, charger votre CV en format .pdf", type=['pdf'], accept_multiple_files=False,label_visibility="visible")
    if uploaded_cv is not None:
        st.session_state['uploaded_cv'] = uploaded_cv
        cv_filename = uploaded_cv.name
        st.session_state['cv_filename'] = cv_filename

        cv_text = read_pdf(uploaded_cv)
        cv_json = analyze_cv(cv_text)
        st.session_state['cv_json'] = cv_json
        st.write(cv_json) # print pour debuggage
