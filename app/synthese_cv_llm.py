import os
import sys
import streamlit as st

# Définition du chemin du répertoire courant
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '..', 'ia')))
from ia import read_pdf, analyze_cv

def synthese_cv_llm():
    st.title("Sythèse du CV via Mistral LLM")
