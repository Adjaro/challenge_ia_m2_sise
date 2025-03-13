from PyPDF2 import PdfReader
import os
import litellm
from dotenv import load_dotenv, find_dotenv
from sentence_transformers import SentenceTransformer, util
import numpy as np


load_dotenv()


def read_pdf(file_path: str) -> str:
    """Lit et extrait le texte d'un CV au format PDF d'une seule page.

    Args:
        file_path (str): Chemin d'accès vers le fichier PDF à lire

    Returns:
        str: Texte brut extrait du PDF

    Raises:
        FileNotFoundError: Si le fichier PDF n'existe pas
        IndexError: Si le PDF est vide
        Exception: Pour toute autre erreur lors de la lecture du PDF
    """
    try:
        reader = PdfReader(file_path)
        if len(reader.pages) == 0:
            raise IndexError("Le PDF est vide")

        page = reader.pages[0]  # Lecture de la première page uniquement
        text_brut = page.extract_text()

        if not text_brut:
            raise Exception("Aucun texte n'a pu être extrait du PDF")

        return text_brut

    except FileNotFoundError:
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
    except IndexError as e:
        raise IndexError(str(e))
    except Exception as e:
        raise Exception(f"Erreur lors de la lecture du PDF: {str(e)}")


# print(read_pdf("CV_V4_EN.pdf"))


def analyze_cv(
    text_brut: str, temperature: float = 0.01, max_tokens: int = 1500
) -> dict:
    """
    Analyse un CV en format texte et retourne les informations structurées en JSON.

    Args:
        text_brut (str): Texte brut du CV à analyser
        temperature (float, optional): Paramètre de créativité du modèle. Defaults to 0.2.
        max_tokens (int, optional): Nombre maximum de tokens pour la réponse. Defaults to 1500.

    Returns:
        dict: Dictionnaire contenant les informations structurées du CV avec les clés suivantes:
            - Diplome: Liste des diplômes avec niveau et domaine d'études
            - Competences: Liste des compétences
            - Experiences: Liste des expériences professionnelles
            - Profil: Informations sur le profil et la disponibilité

    Raises:
        Exception: En cas d'erreur d'API ou de parsing JSON
    """
    try:
        reformulation_prompt = f"""
        À partir du texte brut d'un CV, extrais les informations suivantes au format JSON. 
        Si une information n'est pas explicitement mentionnée dans le texte, retourne `null` ou une liste vide.
        Ne devine pas les informations manquantes et ne retourne que ce qui est clairement présent dans le texte.

        Format JSON attendu :
        {{
            "Formation": [
                {{
                    "niveau_etudes": "str",  // Ex: "Licence", "Master", "Doctorat"
                    "domaine_etudes": ["str"]  // Ex: ["Informatique", "Mathématiques"]
                }}
            ],
            "Competences": ["str"],  // Ex: ["Python", "Gestion de projet"]
            "Experiences": [
                {{
                    "domaine_activite": ["str"],  // Ex: ["Tech", "Finance"]
                    "poste_occupe": "str",  // Ex: "Développeur Python"
                    "duree": "str"  // Ex: "2 ans"
                }}
            ],
            "Profil": {{
                "titre": "str",  // Ex: "Développeur Full-Stack"
                "disponibilite": "str"  // Ex: "Immédiate"
            }}
        }}

        Texte du CV :
        "{text_brut}"

        Ne retourne que le JSON, sans commentaires supplémentaires.
        """

        CV_reformuler = litellm.completion(
            model="mistral/mistral-medium",
            messages=[{"role": "user", "content": reformulation_prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            api_key=os.getenv("MISTRAL_API_KEY"),
        )

        # Extraire et parser le JSON de la réponse
        resultat = CV_reformuler["choices"][0]["message"]["content"].strip()
        return resultat

    except Exception as e:
        raise Exception(f"Erreur lors de l'analyse du CV: {str(e)}")


# print(analyze_cv(text_brut))


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calcule la similarité cosinus entre deux textes en utilisant Sentence-BERT.

    Args:
        text1 (str): Premier texte.
        text2 (str): Deuxième texte.

    Returns:
        float: Score de similarité cosinus entre les deux textes.
    """
    # Encoder les textes en embeddings
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

    embedding1 = model.encode(text1, convert_to_tensor=True)
    embedding2 = model.encode(text2, convert_to_tensor=True)

    # Calculer la similarité cosinus
    similarity = util.cos_sim(embedding1, embedding2)
    return similarity.item()


#### Transformation de l'offre d'emploi au même format que le CV
def analyze_cv_offre_emploi(
    offre: str, temperature: float = 0.01, max_tokens: int = 1500
) -> str:
    """
    Analyse une offre d'emploi en format texte et retourne les informations structurées en JSON.

    Args:
        text_brut (str): Texte brut del'offre à analyser
        temperature (float, optional): Paramètre de créativité du modèle. Defaults to 0.2.
        max_tokens (int, optional): Nombre maximum de tokens pour la réponse. Defaults to 1500.

    Returns:
        str: Informations en string(réponse du LLM) structurées du CV au format JSON

    Raises:
        Exception: En cas d'erreur d'API ou de parsing JSON
    """
    try:
        reformulation_prompt = f"""
        À partir de cette offre d'emploi, extrais les informations suivantes au format JSON. 
        Si une information n'est pas explicitement mentionnée dans le texte, retourne `null` ou une liste vide.
        Ne devine pas les informations manquantes et ne retourne que ce qui est clairement présent dans le texte.

        Format JSON attendu :
        {{
            "Formation": [
                {{
                    "niveau_etudes": "str",  // Ex: "Licence", "Master", "Doctorat"
                    "domaine_etudes": ["str"]  // Ex: ["Informatique", "Mathématiques"]
                }}
            ],
            "Competences": ["str"],  // Ex: ["Python", "Gestion de projet"]
            "Experiences": [
                {{
                    "domaine_activite": ["str"],  // Ex: ["Tech", "Finance"]
                    "poste_occupe": "str",  // Ex: "Développeur Python"
                    "duree": "str"  // Ex: "2 ans"
                }}
            ],
            "Profil": {{
                "titre": "str",  // Ex: "Développeur Full-Stack"
                "disponibilite": "str"  // Ex: "Immédiate"
            }}
        }}

        Texte de l'offre d'emploi :
        "{offre}"

        Ne retourne que le JSON, sans commentaires supplémentaires.
        """

        offre_reformuler = litellm.completion(
            model="mistral/mistral-medium",
            messages=[{"role": "user", "content": reformulation_prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            api_key=os.getenv("MISTRAL_API_KEY"),
        )

        # Extraire et parser le JSON de la réponse
        resultat = offre_reformuler["choices"][0]["message"]["content"].strip()
        return resultat

    except Exception as e:
        raise Exception(f"Erreur lors de l'analyse du CV: {str(e)}")


# print(offre_emploi_to_json(offre))


# Example usage
if __name__ == "__main__":
    file_path = "CV_V4_EN.pdf"
    text = read_pdf(file_path)
    cv_info = analyze_cv(text)
    # score = score_cv_against_job(cv_info, job_offer)
    # print(f"Score de correspondance: {score}")
