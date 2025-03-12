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

# Chargement des pages
if page == "Accueil":
    homepage()
elif page == "CV":
    st.title("Page CV")
elif page == "Offre":
    st.title("Page Offre")
elif page == "Matching":
    st.title("Page Matching")
