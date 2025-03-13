import re
import os
import tempfile
import litellm
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
        Génère un CV optimisé basé sur le CV original et la description du poste.
        
        Args:
            cv_text (str): Texte du CV original
            job_description (str): Description du poste
            
        Returns:
            str: CV optimisé formaté
        """
        prompt = f"""
        À partir du texte suivant d'un CV et de la description d'une offre d'emploi, génère un CV optimisé pour correspondre au mieux à l'offre. Assure-toi d'inclure des sections bien définies et formatées :

        **Sections attendues :**
        - 📌 **Profil** : Un résumé clair et concis du candidat.
        - 🎓 **Formation** : Diplômes et certifications pertinents.
        - 💼 **Expériences professionnelles** : Expériences les plus pertinentes pour l'offre.
        - 🛠 **Compétences** : Liste des compétences techniques et comportementales.
        - 🏆 **Projets & Réalisations** (optionnel) : Principaux projets réalisés en lien avec l'offre.

        **CV Original :**
        {cv_text}

        **Offre d'emploi :**
        {job_description}

        **Nouveau CV optimisé :**
        """
        
        response = litellm.completion(
            model="mistral/mistral-medium",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.01,
            api_key=self.mistral_api_key,
        )
        
        return response["choices"][0]["message"]["content"].strip()
    
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
    
    
    def export_to_pdf(self, optimized_cv):
        """
        Génère un PDF stylisé à partir du CV optimisé en utilisant WeasyPrint avec HTML/CSS.
        
        Args:
            optimized_cv (str): Texte du CV optimisé
            
        Returns:
            str: Chemin vers le fichier PDF créé
        """
        html_template = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    padding: 20px;
                    color: #333;
                }}
                h1 {{
                    color: #2C3E50;
                    text-align: center;
                }}
                .section {{
                    margin-bottom: 20px;
                    padding: 15px;
                    border-left: 5px solid #3498DB;
                    background: #ECF0F1;
                }}
                .section h2 {{
                    color: #2980B9;
                }}
                p {{
                    font-size: 14px;
                    line-height: 1.5;
                }}
            </style>
        </head>
        <body>
            <h1>📄 CV Optimisé</h1>
            
            {"".join(f'<div class="section"><h2>{line}</h2></div>' if line.startswith(("📌", "🎓", "💼", "🛠", "🏆")) else f'<p>{line}</p>' for line in optimized_cv.split("\n\n"))}
        
        </body>
        </html>
        """

        # Générer un fichier temporaire PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as pdf_file:
            HTML(string=html_template).write_pdf(pdf_file.name)
            return pdf_file.name