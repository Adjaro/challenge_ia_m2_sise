from PyPDF2 import PdfReader
import os
import litellm
from dotenv import load_dotenv, find_dotenv
import numpy as np
import requests
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import locale
from monitoring_ecologie import EnvironmentMetrics
import json

load_dotenv()

# Créer une instance unique de monitoring -> A discuter avec Alexis comment implémenter dans son streamlit (cache, session ?)
monitoring_environnement = EnvironmentMetrics()


##########
# Le processus est le suivant :
# 1. Lire un CV au format PDF
# 2. Analyser le CV pour extraire les informations structurées
# 3. Calculer la similarité globale entre le CV et une offre d'emploi
# 4. Analyser une offre d'emploi pour extraire les informations structurées
# 5. Calculer les similarités pour chaque section du CV et de l'offre d'emploi
# 6. Extraires les informations personnelles d'un CV
# 7. Générer une lettre de motivation personnalisée
#
##########

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



############################### Monitoring ###############################


def get_energy_usage(response: litellm.ModelResponse):
    """
    Extracts energy usage and global warming potential (GWP) from the response.

    Parameters:
        response (litellm.ModelResponse): The model response containing impact data.

    Returns:
        tuple: A tuple (energy_usage, gwp) if impacts are present, otherwise (None, None).
    """
    if hasattr(response, "impacts"):
        try:
            energy_usage = getattr(
                response.impacts.energy.value, "min", response.impacts.energy.value
            )
        except AttributeError:
            energy_usage = None

        try:
            gwp = getattr(
                response.impacts.gwp.value, "min", response.impacts.gwp.value
            )
        except AttributeError:
            gwp = None

        return energy_usage, gwp

    return None, None

############################### FIN Monitoring ###############################


def analyze_cv(text_brut: str, temperature: float = 0.01, max_tokens: int = 1500) -> str:
    """
    Analyse un CV en format texte et retourne les informations structurées en JSON.

    Args:
        text_brut (str): Texte brut du CV à analyser
        temperature (float, optional): Paramètre de créativité du modèle. Defaults to 0.2.
        max_tokens (int, optional): Nombre maximum de tokens pour la réponse. Defaults to 1500.

    Returns:
        str: Informations en string(réponse du LLM) structurées du CV au format JSON

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
                "disponibilite": "str"  // Ex: "dd-mm-yyyy"
            }}
        }}

        Texte du CV :
        "{text_brut}"

        Ne retourne que le JSON, sans commentaires supplémentaires.
        """

        response = litellm.completion(
            model="mistral/mistral-medium",
            messages=[{"role": "user", "content": reformulation_prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
            api_key=os.getenv("MISTRAL_API_KEY"),
        )

        # Extraire et parser le JSON de la réponse
        resultat = response["choices"][0]["message"]["content"].strip()

        # Impact écologique
        energy_usage, gwp = get_energy_usage(response=response)
        
        monitoring_environnement.update_metrics(new_gwp=gwp, new_energy=energy_usage)

        # Ajout à une variable globale pour utilisation ultérieure ?

        return resultat
    
    except Exception as e:
        raise Exception(f"Erreur lors de l'analyse du CV: {str(e)}")


# print(analyze_cv(text_brut))

def get_embedding(text: str) -> np.ndarray:
    """
    Envoie une requête à l'API Hugging Face pour obtenir l'embedding d'un texte.

    Args:
        text (str): Texte à encoder.

    Returns:
        np.ndarray: Embedding du texte.
    """
    headers = {"Authorization": f"Bearer {os.getenv("HF_TOKEN")}"}
    response = requests.post(
        "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        headers=headers,
        json={"inputs": text, "options": {"wait_for_model": True}},
    )
    if response.status_code != 200:
        raise Exception(f"Erreur API : {response.status_code}, {response.text}")
    return np.array(response.json())


def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calcule la similarité cosinus entre deux textes en utilisant l'API Hugging Face.

    Args:
        text1 (str): Premier texte.
        text2 (str): Deuxième texte.

    Returns:
        float: Score de similarité cosinus entre les deux textes.
    """
    # Obtenir les embeddings des textes
    embedding1 = get_embedding(text1)
    embedding2 = get_embedding(text2)

    # Calculer la similarité cosinus
    similarity = cosine_similarity([embedding1], [embedding2])[0][0]
    return similarity


# # Calculer la similarité entre le CV et l'offre d'emploi
# similarity_score = calculate_similarity(CV_reformuler, job_offer_reforumer)
# print(f"Similarité globale entre le CV et l'offre d'emploi: {similarity_score:.4f}")


#### Transformation de l'offre d'emploi au même format que le CV
def analyze_offre_emploi(offre: str, temperature: float = 0.01, max_tokens: int = 1500) -> str:
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
        De plus la disponibilité correspond à la date de début du poste.
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
                "disponibilite": "str"  // Ex: "dd-mm-yyyy"
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

        # Impact écologique
        energy_usage, gwp = get_energy_usage(response=offre_reformuler)
        monitoring_environnement.update_metrics(new_gwp=gwp, new_energy=energy_usage)

        return resultat
    
    except Exception as e:
        raise Exception(f"Erreur lors de l'analyse du CV: {str(e)}")


# print(offre_emploi_to_json(offre))

def calculate_section_similarity(cv_reformule: str, offre_emploi_reformule: str) -> dict:
    """
    Calcule les similarités détaillées entre les différentes sections d'un CV et une offre d'emploi.
    
    Args:
        cv_reformule (str): Informations du CV au format JSON string
        offre_emploi_reformule (str): Informations de l'offre d'emploi au format JSON string
        
    Returns:
        dict: Dictionnaire contenant les scores de similarité pour chaque section
        
    Exemple:
        {
            'formation': float,
            'competences': float,
            'experiences': float,
            'profil': float,
        }
    """
    try:
        # Conversion des chaînes JSON en dictionnaires
        cv_json = json.loads(cv_reformule)
        offre_emploi_json = json.loads(offre_emploi_reformule)
        
        # Calcul des similarités pour chaque section
        similarites = {}
        
        # Similarité de formation
        formation_candidat = cv_json.get("Formation", "")
        formation_attendue = offre_emploi_json.get("Formation", "")
        similarites['formation'] = calculate_similarity(
            str(formation_candidat), 
            str(formation_attendue)
        )
        
        # Similarité des compétences
        competences_candidat = cv_json.get("Competences", [])
        competences_attendues = offre_emploi_json.get("Competences", [])
        similarites['competences'] = calculate_similarity(
            str(competences_candidat), 
            str(competences_attendues)
        )
        
        # Similarité des expériences
        experiences_candidat = cv_json.get("Experiences", [])
        experiences_attendues = offre_emploi_json.get("Experiences", [])
        similarites['experiences'] = calculate_similarity(
            str(experiences_candidat), 
            str(experiences_attendues)
        )
        
        # Similarité du profil
        profil_candidat = cv_json.get("Profil", {})
        profil_attendu = offre_emploi_json.get("Profil", {})
        similarites['profil'] = calculate_similarity(
            str(profil_candidat), 
            str(profil_attendu)
        )
        
        return similarites
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Erreur lors du parsing JSON : {str(e)}")
    except Exception as e:
        raise Exception(f"Erreur lors du calcul des similarités : {str(e)}")

# calculate_section_similarity(CV_reformuler, job_offer_reforumer)
# print(calculate_section_similarity(CV_reformuler, job_offer_reforumer)['formation'])

def extraction_info_perso(text_brut: str) -> str:
    """
    Extrait les informations personnelles d'un CV en format texte brut.

    Args:
        text_brut (str): Texte brut du CV à analyser

    Returns:
        str: Informations personnelles extraites du CV en format JSON like
    """

    prompt_extraction_info_perso = f"""
    Extrait les informations personnelles suivantes du texte brut d'un CV et retourne-les au format JSON :
    - Nom et prénom
    - Email
    - Numéro de téléphone
    - Adresse

    Si une information est manquante, retourne `Non réseigner` pour cette clé.

    Texte brut du CV :
    "{text_brut}"

    Format JSON attendu :
    {{
        "nom_prenom": "str",
        "email": "str",
        "telephone": "str",
        "adresse": "str"
    }}

    Ne retourne que le JSON, sans commentaires supplémentaires.
    """
    resultat_extraction_info_perso = litellm.completion(
                model="mistral/mistral-tiny",  
                messages=[{"role": "user", "content": prompt_extraction_info_perso}],
                max_tokens=100,
                temperature=0.1,
                api_key=os.getenv("MISTRAL_API_KEY"),
            )
    
    # Impact écologique
    energy_usage, gwp = get_energy_usage(response=resultat_extraction_info_perso)
    monitoring_environnement.update_metrics(new_gwp=gwp, new_energy=energy_usage)
    
    return resultat_extraction_info_perso["choices"][0]["message"]["content"].strip()
    
    
    
# print(extraction_info_perso(text_brut))


def generate_lettre_motivation(text_brut: str, job_offer:str) ->str:
    """
    Génère une lettre de motivation personnalisée en fonction des informations extraites du CV et de l'offre d'emploi.
    
    Args:
        text_brut (str): Texte brut extrait du CV du candidat
        job_offer (str): Description de l'offre d'emploi
        
    Returns:
        str: Lettre de motivation générée au format texte
    
    """
    information_perso = extraction_info_perso(text_brut)
    resultat_extraction_info_perso_json = json.loads(information_perso)

    nom = resultat_extraction_info_perso_json.get("nom_prenom")
    email = resultat_extraction_info_perso_json.get("email", "").strip()
    # Remove all spaces from email
    email = "".join(email.split())
    telephone = resultat_extraction_info_perso_json.get("telephone")
    adresse = resultat_extraction_info_perso_json.get("adresse")


    # Set French locale
    try:
        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')  # Linux/Mac
    except:
        locale.setlocale(locale.LC_TIME, 'fra_fra')  # Windows

    # Get date in French format
    date = datetime.now().strftime("%d %B %Y")

    prompt_lettre_motivation = f"""
    Tu es un assistant qui rédige des lettres de motivation personnalisées et professionnelles. Voici les informations nécessaires :

    **Informations du candidat :**
    - Nom : {nom}
    - Email : {email}
    - Téléphone : {telephone}
    - Adresse : {adresse}
    - Date : {date}

    **Texte brut du CV :**
    {text_brut}

    **Offre d'emploi :**
    {job_offer}

    **Instructions :**
    1. Rédige une lettre de motivation au format A4, bien structurée et professionnelle.
    2. Mets en avant les compétences et expériences du candidat qui correspondent aux exigences du poste.
    3. Mentionne des éléments spécifiques de l'entreprise ou du poste pour montrer que la candidature est personnalisée.
    4. Explique pourquoi le candidat est motivé pour rejoindre cette entreprise en particulier.
    5. Utilise un ton professionnel et évite les phrases génériques.
    6. Ne laisse pas de champs vides et ne devine pas les informations manquantes.

    **Format de la lettre :**
    - En-tête : Nom, prénom, adresse, email, téléphone, date.
    - Introduction : Présentation du candidat et motivation pour le poste.
    - Corps : Compétences et expériences en lien avec le poste.
    - Conclusion : Expression de l'enthousiasme et disponibilité pour un entretien.

    **Exemple de structure :**
    {nom}
    {email}
    {telephone}
    {adresse}
    {date}

    Madame, Monsieur,
    Je me permets de vous adresser ma candidature pour le poste de [poste] au sein de [entreprise]. [Motivation personnalisée].

    Avec mon expérience en [domaine] et mes compétences en [compétences], je suis convaincu de pouvoir contribuer à [objectif de l'entreprise]. [Détail des expériences et compétences pertinentes].

    Je serais ravi de discuter de ma candidature lors d'un entretien. Je reste à votre disposition pour toute information complémentaire.

    Veuillez agréer, Madame, Monsieur, mes salutations distinguées.
    {nom}
    """
        
    Lettre_motiv_genere = litellm.completion(
                model="mistral/ministral-3b-latest",  
                messages=[{"role": "user", "content": prompt_lettre_motivation}],
                max_tokens=1500,
                temperature=0.3,
                api_key=os.getenv("MISTRAL_API_KEY"),
            )


    # Impact écologique
    energy_usage, gwp = get_energy_usage(response=Lettre_motiv_genere)
    monitoring_environnement.update_metrics(new_gwp=gwp, new_energy=energy_usage)

    resultat = Lettre_motiv_genere["choices"][0]["message"][
                "content"
            ].strip()
    
    return resultat



# print(generate_lettre_motivation(text_brut, job_offer))



# Example usage
if __name__ == "__main__":
    file_path = "CV_V4_EN.pdf"
    text = read_pdf(file_path)
    cv_info = analyze_cv(text)
    # score = score_cv_against_job(cv_info, job_offer)
    # print(f"Score de correspondance: {score}")
