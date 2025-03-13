import re
import os
import tempfile
import litellm
import json
from PyPDF2 import PdfReader
from weasyprint import HTML
from fpdf import FPDF
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class CVGenerator:
    def __init__(self):
        self.mistral_api_key = os.getenv("MISTRAL_API_KEY")
    
    def generate_perfect_cv(self, cv_text, job_description):
        """
        Génère un CV optimisé basé sur le CV original et la description du poste,
        puis structure les données pour être compatible avec notre générateur de PDF.
        """
        # Prompt pour obtenir un CV optimisé structuré
        prompt = f"""
    À partir du texte suivant d'un CV et de la description d'une offre d'emploi, génère un CV optimisé pour correspondre au mieux à l'offre.

    IMPORTANT: La réponse doit être structurée en JSON pour être traitée par un système de génération de PDF. Respecte strictement le format demandé.

    CV Original:
    {cv_text}

    Offre d'emploi:
    {job_description}

    INSTRUCTIONS:
    1. Analyse le CV original et l'offre d'emploi pour identifier les compétences et expériences les plus pertinentes.
    2. Génère un CV optimisé qui met en valeur ces éléments.
    3. Retourne ta réponse UNIQUEMENT au format JSON suivant, sans aucun texte avant ou après:

    ```json
    {{
    "prenom": "Prénom",
    "nom": "NOM",
    "titre": "TITRE DU POSTE",
    "objectif": "Texte décrivant l'objectif professionnel, adapté à l'offre d'emploi (maximum 4 lignes)",
    "competences": [
        "Compétence 1",
        "Compétence 2",
        "Compétence 3",
        "Compétence 4",
        "Compétence 5",
        "Compétence 6",
        "Compétence 7"
    ],
    "interets": [
        "Intérêt 1",
        "Intérêt 2"
    ],
    "contacts": [
        {{"icon": "📞", "value": "Numéro de téléphone"}},
        {{"icon": "✉️", "value": "Adresse email"}},
        {{"icon": "📍", "value": "Adresse postale"}}
    ],
    "experiences": [
        {{
        "date": "MM/AAAA - MM/AAAA",
        "titre": "Nom de l'entreprise",
        "lieu": "Ville",
        "details": [
            "Description détaillée de la responsabilité 1",
            "Description détaillée de la responsabilité 2",
            "Description détaillée de la responsabilité 3"
        ]
        }},
        {{
        "date": "MM/AAAA - MM/AAAA",
        "titre": "Nom de l'entreprise",
        "lieu": "Ville",
        "details": [
            "Description détaillée de la responsabilité 1",
            "Description détaillée de la responsabilité 2"
        ]
        }}
    ],
    "formation": [
        {{
        "titre": "Nom du diplôme ou de la formation",
        "institution": "Nom de l'établissement",
        "details": "Détails supplémentaires (spécialisation, mention, etc.)"
        }}
    ]
    }}
    ```

    IMPORTANT: Assure-toi que le JSON est valide et complet, avec les champs exactement comme spécifiés ci-dessus.
    """
        
        response = litellm.completion(
            model="mistral/mistral-medium",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.01,
            api_key=self.mistral_api_key,
        )
        
        cv_data_json = response["choices"][0]["message"]["content"].strip()
        
        # Extraction du JSON (au cas où il y aurait du texte avant/après)
        json_pattern = r'```json\s*([\s\S]*?)\s*```'
        match = re.search(json_pattern, cv_data_json)
        
        if match:
            cv_data_json = match.group(1)
        else:
            # Si pas de balises code, essayer de trouver directement le JSON
            json_pattern = r'^\s*{\s*"prenom":'
            match = re.search(json_pattern, cv_data_json)
            if match:
                cv_data_json = cv_data_json
        
        try:
            # Analyse du JSON
            cv_data = json.loads(cv_data_json)
            return cv_data
        except json.JSONDecodeError as e:
            # En cas d'erreur de décodage JSON
            print(f"Erreur de décodage JSON: {e}")
            print(f"Contenu reçu: {cv_data_json}")
            # Retourner une structure minimale
            return {
                "prenom": "Erreur",
                "nom": "De Format",
                "titre": "ERREUR DE PARSING JSON",
                "objectif": "Une erreur s'est produite lors de l'analyse de la réponse. Veuillez réessayer.",
                "competences": ["Erreur de formatage"],
                "interets": ["Erreur de formatage"],
                "contacts": [{"icon": "⚠️", "value": "Erreur de formatage"}],
                "experiences": [{"date": "", "titre": "Erreur", "lieu": "", "details": ["Erreur de formatage"]}],
                "formation": [{"titre": "Erreur", "institution": "", "details": "Erreur de formatage"}]
            }

    def clean_text(self, text):
        """
        Nettoie le texte en supprimant les emojis et caractères spéciaux non supportés par fpdf.
        
        Args:
            text (str): Texte à nettoyer
            
        Returns:
            str: Texte nettoyé
        """
        text = re.sub(r'[\U00010000-\U0010ffff]', '', text)  # Supprime les emojis
        text = text.encode('latin-1', 'ignore').decode('latin-1')  # Supprime les caractères non supportés
        return text
    
    def export_cv_to_pdf(self, cv_data, output_path=None):
        """
        Génère un PDF de CV suivant un modèle deux colonnes.
        
        Args:
            cv_data (dict): Dictionnaire contenant les données du CV
            output_path (str, optional): Chemin de sortie pour le PDF. Si None, crée un fichier temporaire.
            
        Returns:
            str: Chemin vers le fichier PDF généré
        """
        # Style CSS pour un CV professionnel avec deux colonnes
        css = """
            @page {
                size: A4;
                margin: 0;
            }
            body {
                font-family: 'Arial', 'Helvetica', sans-serif;
                margin: 0;
                padding: 0;
                color: #333;
                line-height: 1.5;
            }
            .cv-container {
                display: flex;
                width: 100%;
                height: 100%;
            }
            .left-column {
                width: 30%;
                background-color: #0e5e73;
                color: white;
                padding: 30px 20px;
            }
            .right-column {
                width: 70%;
                padding: 30px 20px;
            }
            .profile-image {
                width: 100%;
                margin-bottom: 20px;
                text-align: center;
            }
            .profile-image img {
                width: 80%;
                border: 3px solid white;
            }
            h1 {
                color: #0e5e73;
                font-size: 38px;
                margin: 0;
                font-weight: bold;
                line-height: 1.1;
            }
            h1 .lastname {
                color: black;
            }
            .job-title {
                font-size: 18px;
                color: #666;
                margin-top: 5px;
                margin-bottom: 25px;
                text-transform: uppercase;
            }
            .contact-info {
                margin-bottom: 30px;
            }
            .contact-item {
                display: flex;
                align-items: center;
                margin-bottom: 10px;
            }
            .contact-icon {
                margin-right: 10px;
                width: 20px;
            }
            .section-title {
                font-size: 18px;
                text-transform: uppercase;
                font-weight: bold;
                color: white;
                margin-top: 30px;
                margin-bottom: 15px;
                padding-bottom: 5px;
                border-bottom: 2px solid white;
            }
            .right-section-title {
                font-size: 18px;
                text-transform: uppercase;
                font-weight: bold;
                color: #0e5e73;
                margin-top: 30px;
                margin-bottom: 15px;
                padding-bottom: 5px;
                border-bottom: 2px solid #0e5e73;
            }
            .skill-item, .interest-item {
                margin-bottom: 8px;
            }
            .experience {
                margin-bottom: 20px;
            }
            .experience-header {
                margin-bottom: 10px;
            }
            .experience-date {
                color: #666;
                font-weight: bold;
            }
            .experience-title {
                font-weight: bold;
            }
            .experience-location {
                font-style: italic;
            }
            .experience-details {
                margin-left: 15px;
            }
            .experience-details ul {
                margin: 0;
                padding-left: 20px;
            }
            .experience-details li {
                margin-bottom: 5px;
            }
            .education {
                margin-bottom: 20px;
            }
            .education-title {
                font-weight: bold;
            }
            .education-institution {
                font-style: italic;
            }
            .education-details {
                margin-top: 5px;
            }
        """
        
        # Création du HTML basé sur les données fournies
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{cv_data['prenom']} {cv_data['nom']} - CV</title>
            <style>
                {css}
            </style>
        </head>
        <body>
            <div class="cv-container">
                <div class="left-column">
                    <!-- Photo de profil (optionnelle) -->
                    {f'<div class="profile-image"><img src="{cv_data["photo"]}" alt="Photo de profil"></div>' if "photo" in cv_data else ''}
                    
                    <!-- Section Objectif -->
                    <div class="section-title">OBJECTIF PROFESSIONNEL</div>
                    <div class="objective">
                        {cv_data['objectif']}
                    </div>
                    
                    <!-- Section Compétences -->
                    <div class="section-title">COMPÉTENCES</div>
                    <div class="skills">
        """
        
        # Ajouter les compétences
        for skill in cv_data['competences']:
            html_content += f'                <div class="skill-item">• {skill}</div>\n'
        
        html_content += """
                    </div>
                    
                    <!-- Section Centres d'intérêt -->
                    <div class="section-title">CENTRES D'INTÉRÊT</div>
                    <div class="interests">
        """
        
        # Ajouter les centres d'intérêt
        for interest in cv_data['interets']:
            html_content += f'                <div class="interest-item">• {interest}</div>\n'
        
        html_content += f"""
                    </div>
                </div>
                
                <div class="right-column">
                    <!-- Nom et titre -->
                    <h1><span class="firstname">{cv_data['prenom']}</span> <span class="lastname">{cv_data['nom']}</span></h1>
                    <div class="job-title">{cv_data['titre']}</div>
                    
                    <!-- Informations de contact -->
                    <div class="contact-info">
        """
        
        # Ajouter les informations de contact
        for contact in cv_data['contacts']:
            html_content += f"""
                        <div class="contact-item">
                            <div class="contact-icon">{contact['icon']}</div>
                            <div>{contact['value']}</div>
                        </div>
            """
        
        html_content += """
                    </div>
                    
                    <!-- Section Expériences professionnelles -->
                    <div class="right-section-title">EXPÉRIENCES PROFESSIONNELLES</div>
        """
        
        # Ajouter les expériences professionnelles
        for exp in cv_data['experiences']:
            html_content += f"""
                    <div class="experience">
                        <div class="experience-header">
                            <div class="experience-date">{exp['date']}</div>
                            <div class="experience-title">{exp['titre']}</div>
                            <div class="experience-location">{exp['lieu']}</div>
                        </div>
                        <div class="experience-details">
                            <ul>
            """
            
            for detail in exp['details']:
                html_content += f'                            <li>{detail}</li>\n'
            
            html_content += """
                            </ul>
                        </div>
                    </div>
            """
        
        html_content += """
                    <!-- Section Formation -->
                    <div class="right-section-title">FORMATION</div>
        """
        
        # Ajouter les formations
        for edu in cv_data['formation']:
            html_content += f"""
                    <div class="education">
                        <div class="education-title">{edu['titre']}</div>
                        <div class="education-institution">{edu['institution']}</div>
                        <div class="education-details">{edu['details']}</div>
                    </div>
            """
        
        html_content += """
                </div>
            </div>
        </body>
        </html>
        """
        
        # Déterminer le chemin de sortie
        if output_path is None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
                output_path = pdf_file.name
        
        # Générer le PDF
        HTML(string=html_content).write_pdf(output_path)
        return output_path