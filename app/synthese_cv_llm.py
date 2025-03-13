import os
import sys
import streamlit as st
import json

# Définition du chemin du répertoire courant
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', 'ia')))
from ia import read_pdf, analyze_cv

def synthese_cv_llm():
    st.title("📄 Synthèse du CV via Mistral LLM")
    
    # Vérification de l'upload du CV
    if st.session_state.get('uploaded_cv') is None :
        st.write("Veuillez charger un CV pour lancer l'analyse")

    else :
        uploaded_cv = st.session_state.get('uploaded_cv')
        text_brut = read_pdf(uploaded_cv)

        # Analyse du CV
        dict_cv = analyze_cv(text_brut)
        data = json.loads(dict_cv)

        # Profil
        title_container = st.container(border=True,height=60)
        with title_container:
            st.markdown(
                f"<div style='display: flex; justify-content: space-between; align-items: center; height: 100%;'>"
                f"<span style='font-weight: bold;'>👤 {data['Profil']['titre']}</span>"
                f"<span style='font-style: italic;'>🕒 {data['Profil']['disponibilite']}</span>"
                f"</div>",
                unsafe_allow_html=True
            )

        # Diplômes
        st.header("🎓 Diplômes")
        for diplome in data["Diplome"]:
            st.subheader(diplome["niveau_etudes"])
            st.write(f"Domaine : {', '.join(diplome['domaine_etudes'])}")

        # Compétences
        st.header("🛠️ Compétences")
        st.write(" | ".join(data["Competences"]))

        # Expériences
        st.header("💼 Expériences")
        for experience in data["Experiences"]:
            st.subheader(experience["poste_occupe"])
            st.write(f"Secteurs : {', '.join(experience['domaine_activite'])}")
            if experience["duree"]:
                st.write(f"Durée : {experience['duree']}")
