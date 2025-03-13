"""
Ce fichier contient les fonctions nécessaires pour l'affichage de l'interface de l'application.
"""

import os
import streamlit as st
from PIL import Image  # Pour gérer l'image du logo

# Chemin vers le logo (à adapter selon votre structure de projet)
LOGO_PATH = "logo.png"

def set_custom_style():
    """
    Définit le style personnalisé de l'application.
    """
    st.markdown("""
        <style>
        .stButton button {
            border-radius: 10px;
            transition: transform 0.2s;
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
        }
        .stButton button:hover {
            transform: scale(1.05);
            background-color: #45a049;
        }
        .sidebar .stTitle {
            color: #2E4057;
            padding-bottom: 20px;
        }
        .stExpander {
            border: 1px solid #ddd;
            border-radius: 10px;
            margin-bottom: 10px;
        }
        .stExpander:hover {
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .scrollable-container {
            height: 25vh; /* 25% de la hauteur de la fenêtre */
            overflow-y: auto; /* Permet le défilement vertical */
            border: 1px solid #ddd;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def load_logo():
    """
    Charge et affiche le logo de l'application.
    """
    if os.path.exists(LOGO_PATH):
        logo = Image.open(LOGO_PATH)
        st.sidebar.image(logo, use_column_width=True)
    else:
        st.sidebar.markdown("### 🚀 CV Matcher")

@st.dialog("Modification du profil", width="large")
def show_modif_profile_dialog(profil: dict):
    """
    Affiche un dialogue pour modifier les informations du profil.
    """
    st.markdown("### 📋 Modification du profil")
    st.markdown("---")
    profil["titre"] = st.text_input("Titre", profil.get("titre", ""))
    profil["disponibilite"] = st.text_input("Disponibilité", profil.get("disponibilite", ""))
    if st.button("Enregistrer les modifications"):
        st.success("Profil mis à jour avec succès !")

@st.dialog("Modification de la formation", width="large")
def show_modif_formation_dialog(formations: list):
    """
    Affiche un dialogue pour modifier les informations de formation.
    """
    st.markdown("### 📋 Modification de la formation")
    st.markdown("---")
    for i, formation in enumerate(formations):
        with st.expander(f"Formation {i+1}"):
            formation["niveau_etudes"] = st.text_input("Niveau d'études", formation.get("niveau_etudes", ""), key=f"niveau_etudes_{i}")
            formation["domaine_etudes"] = st.text_input("Domaine d'études", ", ".join(formation.get("domaine_etudes", [])), key=f"domaine_etudes_{i}")
    if st.button("Enregistrer les modifications"):
        st.success("Formations mises à jour avec succès !")

@st.dialog("Modification des compétences", width="large")
def show_modif_competences_dialog(competences: list):
    """
    Affiche un dialogue pour modifier les compétences.
    """
    st.markdown("### 📋 Modification des compétences")
    st.markdown("---")
    competences_str = st.text_area("Compétences", ", ".join(competences))
    if st.button("Enregistrer les modifications"):
        competences[:] = [c.strip() for c in competences_str.split(",")]
        st.success("Compétences mises à jour avec succès !")

@st.dialog("Modification des expériences", width="large")
def show_modif_experiences_dialog(experiences: list):
    """
    Affiche un dialogue pour modifier les expériences.
    """
    st.markdown("### 📋 Modification des expériences")
    st.markdown("---")
    for i, experience in enumerate(experiences):
        with st.expander(f"Expérience {i+1}"):
            experience["poste_occupe"] = st.text_input("Poste occupé", experience.get("poste_occupe", ""), key=f"poste_occupe_{i}")
            experience["domaine_activite"] = st.text_input("Domaine d'activité", ", ".join(experience.get("domaine_activite", [])), key=f"domaine_activite_{i}")
            experience["duree"] = st.text_input("Durée", experience.get("duree", ""), key=f"duree_{i}")
    if st.button("Enregistrer les modifications"):
        st.success("Expériences mises à jour avec succès !")

def show_sidebar(cv_info: dict) -> str:
    """
    Affiche la barre latérale de l'application avec les informations du CV.

    Args:
        cv_info (dict): Dictionnaire contenant les informations du CV.

    Returns:
        str: Nom de la conversation sélectionnée.
    """
    set_custom_style()
    load_logo()  # Charger le logo

    with st.sidebar:
        st.markdown("---")

        # Section Profil
        st.markdown("### 👤 Profil")
        with st.container():
            st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
            st.write(f"**Titre:** {cv_info['Profil'].get('titre', 'Non renseigné')}")
            st.write(f"**Disponibilité:** {cv_info['Profil'].get('disponibilite', 'Non renseigné')}")
            if st.button("Modifier le profil", key="modif_profil"):
                show_modif_profile_dialog(cv_info["Profil"])
            st.markdown('</div>', unsafe_allow_html=True)

        # Section Formation
        st.markdown("### 🎓 Formation")
        with st.container():
            st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
            for i, formation in enumerate(cv_info.get("Formation", [])):
                with st.expander(f"Formation {i+1}"):
                    st.write(f"**Niveau d'études:** {formation.get('niveau_etudes', 'Non renseigné')}")
                    st.write(f"**Domaine d'études:** {', '.join(formation.get('domaine_etudes', []))}")
            if st.button("Modifier les formations", key="modif_formation"):
                show_modif_formation_dialog(cv_info["Formation"])
            st.markdown('</div>', unsafe_allow_html=True)

        # Section Compétences
        st.markdown("### 🛠️ Compétences")
        with st.container():
            st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
            st.write(", ".join(cv_info.get("Competences", [])))
            if st.button("Modifier les compétences", key="modif_competences"):
                show_modif_competences_dialog(cv_info["Competences"])
            st.markdown('</div>', unsafe_allow_html=True)

        # Section Expériences
        st.markdown("### 💼 Expériences")
        with st.container():
            st.markdown('<div class="scrollable-container">', unsafe_allow_html=True)
            for i, experience in enumerate(cv_info.get("Experiences", [])):
                with st.expander(f"Expérience {i+1}"):
                    st.write(f"**Poste occupé:** {experience.get('poste_occupe', 'Non renseigné')}")
                    st.write(f"**Domaine d'activité:** {', '.join(experience.get('domaine_activite', []))}")
                    st.write(f"**Durée:** {experience.get('duree', 'Non renseigné')}")
            if st.button("Modifier les expériences", key="modif_experiences"):
                show_modif_experiences_dialog(cv_info["Experiences"])
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("---")
        header_cols = st.columns([3, 1, 1])
        with header_cols[0]:
            st.header("💬 Conversations")
        with header_cols[1]:
            if st.button("📊", help="Voir les statistiques", use_container_width=True):
                st.write("Statistiques à implémenter...")

# Exemple de données CV
cv_info = {
    "Profil": {
        "titre": "Data Scientist",
        "disponibilite": "Disponible immédiatement"
    },
    "Formation": [
        {
            "niveau_etudes": "Master",
            "domaine_etudes": ["Informatique", "Mathématiques appliquées"]
        }
    ],
    "Competences": [
        "Python", "SQL", "Terraform", "Bitbucket", "Jenkins", "Airflow", "Docker", 
        "Kubernetes", "GCP (BigQuery, Spark DataProc)", "Développement logiciel agile", 
        "Algorithmes d'apprentissage statistique"
    ],
    "Experiences": [
        {
            "domaine_activite": ["Data Science"],
            "poste_occupe": "Data Scientist",
            "duree": "5 ans"
        }
    ]
}

# Affichage de la barre latérale
show_sidebar(cv_info)