"""
Ce fichier contient les fonctions nécessaires pour l'affichage de l'interface de l'application.
"""

import os
import streamlit as st
from PIL import Image

LOGO_PATH = "logo.png"

def set_custom_style():
    """
    Définit le style personnalisé de l'application avec des couleurs et designs améliorés.
    """
    st.markdown("""
        <style>
        /* Base styles */
        .main {
            padding: 2rem;
        }
        
        /* Button styles */
        .stButton button {
            border-radius: 8px;
            transition: all 0.3s ease;
            background-color: #2E86C1;
            color: white;
            border: none;
            padding: 10px 24px;
            font-weight: 500;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton button:hover {
            transform: translateY(-2px);
            background-color: #2874A6;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        
        /* Sidebar styles */
        .sidebar .stTitle {
            color: #2C3E50;
            font-weight: bold;
            margin-bottom: 1.5rem;
        }
        
        /* Expander styles */
        .stExpander {
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            margin-bottom: 1rem;
            background-color: white;
            transition: all 0.3s ease;
        }
        .stExpander:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        
        /* Scrollable container */
        .scrollable-container {
            max-height: 30vh;
            overflow-y: auto;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 1rem;
            margin-bottom: 1.5rem;
            background-color: white;
            box-shadow: inset 0 0 6px rgba(0,0,0,0.05);
        }
        
        /* Section headers */
        .section-header {
            color: #2C3E50;
            font-size: 1.2rem;
            font-weight: 600;
            margin: 1rem 0;
        }
        
        /* Success message */
        .success-message {
            padding: 1rem;
            background-color: #D4EDDA;
            color: #155724;
            border-radius: 8px;
            margin: 1rem 0;
        }
        </style>
    """, unsafe_allow_html=True)

def load_logo():
    """
    Charge et affiche le logo avec gestion d'erreur améliorée.
    """
    try:
        if os.path.exists(LOGO_PATH):
            logo = Image.open(LOGO_PATH)
            st.sidebar.image(logo, use_column_width=True)
        else:
            st.sidebar.title("🚀 CV Matcher")
    except Exception as e:
        st.sidebar.error(f"Erreur de chargement du logo: {str(e)}")

def show_success_message(message: str):
    """
    Affiche un message de succès stylisé.
    """
    st.markdown(f'<div class="success-message">{message}</div>', unsafe_allow_html=True)

@st.cache_data
def format_data_display(data, prefix=""):
    """
    Formate les données pour l'affichage avec une meilleure présentation.
    """
    if isinstance(data, list):
        return ", ".join(str(item) for item in data if item)
    return str(data) if data else "Non renseigné"

def show_modif_dialog(title: str, content_func, on_save=None):
    """
    Fonction générique pour afficher un dialogue de modification.
    """
    with st.form(f"form_{title.lower().replace(' ', '_')}"):
        st.markdown(f"### 📋 {title}")
        st.markdown("---")
        result = content_func()
        if st.form_submit_button("Enregistrer"):
            if on_save:
                on_save(result)
            show_success_message(f"{title} mis à jour avec succès !")
            return True
    return False

# Les fonctions de dialogue existantes peuvent être simplifiées en utilisant show_modif_dialog

def show_sidebar(cv_info: dict) -> None:
    """
    Affiche la barre latérale avec une meilleure organisation et présentation.
    """
    set_custom_style()
    load_logo()

    with st.sidebar:
        st.markdown("---")

        # Sections du CV avec conteneurs scrollables améliorés
        sections = {
            "👤 Profil": ("Profil", lambda x: x.get("titre", "") + "\n" + x.get("disponibilite", "")),
            "🎓 Formation": ("Formation", lambda x: "\n".join([f"{f.get('niveau_etudes', '')}: {format_data_display(f.get('domaine_etudes', []))}" for f in x])),
            "🛠️ Compétences": ("Competences", lambda x: format_data_display(x)),
            "💼 Expériences": ("Experiences", lambda x: "\n".join([f"{e.get('poste_occupe', '')}\n{format_data_display(e.get('domaine_activite', []))}\n{e.get('duree', '')}" for e in x]))
        }

        for title, (key, formatter) in sections.items():
            st.markdown(f"### {title}")
            with st.container():
                st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
                data = cv_info.get(key, [])
                if data:
                    st.markdown(formatter(data))
                if st.button(f"Modifier {title.split()[1]}", key=f"modif_{key.lower()}"):
                    # Ici, vous pouvez appeler vos fonctions de dialogue existantes
                    pass
                st.markdown('</div>', unsafe_allow_html=True)