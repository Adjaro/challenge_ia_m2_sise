import os
import sys
import pandas as pd
import streamlit as st
import requests
from utils.ia import read_pdf, analyze_cv, calculate_similarity
from utils.classFactory import ScrapingFactory
import json
from components import  show_modifier_cv
def homepage():
    # [Garder le code CSS existant...]
    st.session_state["enregistrer_modifications"] = False
    st.markdown("""
        <style>
            .main {
                padding-top: 2rem;
            }
            .title-container {
                display: flex;
                justify-content: center;
                margin-bottom: 2rem;
            }
            .upload-container {
                max-width: 600px;
                margin: 0 auto;
                text-align: center;
                padding: 2rem;
                background-color: #f8f9fa;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
                transition: background-color 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
            .stFileUploader>div>div {
                border: 2px dashed #4CAF50;
                border-radius: 10px;
                padding: 20px;
                background-color: #ffffff;
            }
            .stFileUploader>div>div:hover {
                border-color: #45a049;
            }
            /* Styles pour la boîte de dialogue modale */
            .modal {
                display: none;
                position: fixed;
                z-index: 1000;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                overflow: auto;
                background-color: rgba(0, 0, 0, 0.5);
            }
            .modal-content {
                background-color: white;
                margin: 10% auto;
                padding: 20px;
                border-radius: 10px;
                width: 80%;
                max-width: 600px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .close {
                color: #aaa;
                float: right;
                font-size: 28px;
                font-weight: bold;
            }
            .close:hover,
            .close:focus {
                color: black;
                text-decoration: none;
                cursor: pointer;
            }
        </style>
        """, unsafe_allow_html=True)

    with st.container():
        # [Garder le code du container existant jusqu'au chargement du CV...]
        # Logo et titre centrés
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image("app/logo.png", width=250)  # Remplacez par le chemin de votre logo
            st.title("Bienvenue sur JobMatch")
            st.markdown(
                "<div style='text-align: center;'>"
                "Cette application vous permet d'améliorer votre candidature par rapport à des offres d'emplois qui vous intéressent."
                "</div>",
                unsafe_allow_html=True
            )
        
        # Zone de chargement centrée
        st.markdown('<div> ', unsafe_allow_html=True)
        uploaded_cv = st.file_uploader(
            label="Pour commencer, chargez votre CV en format .pdf",
            type=['pdf'],
            accept_multiple_files=False,
            label_visibility="visible"
        )
        if uploaded_cv is not None:
            st.session_state['uploaded_cv'] = uploaded_cv
            cv_filename = uploaded_cv.name

            st.session_state['cv_filename'] = cv_filename

            cv_text = read_pdf(uploaded_cv)
            cv_json = analyze_cv(cv_text)
            cv_json = json.loads(cv_json)  # Convertir la chaîne JSON en dictionnaire
            #convertir le dictionnaire en json
            cv_json = json.dumps(cv_json)
            st.session_state['cv_json'] = cv_json
            # st.write(cv_json)

            if cv_json:
                st.session_state['charger_csv'] = True
                show_modifier_cv()
            
                # if st.session_state.get('enregistrer_modifications') == True:
                #     st.session_state['page'] = 'next_page'
                #     st.rerun()
                # else:
                #     st.session_state['page'] = 'homepage'
                #     st.rerun()
                # st.rerun()
 