import requests
from bs4 import BeautifulSoup

class ScrapingFrancetravail:
    """
    Classe pour scraper les offres d'emploi sur le site France Travail et interagir avec l'API Pôle Emploi.
    """

    # En-têtes pour imiter un vrai navigateur
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    def __init__(self):
        """
        Initialise la classe avec l'URL de base de France Travail et récupère le token d'accès à l'API.
        """
        self.base_url = "https://www.francetravail.fr"  # URL de base pour France Travail
        self.access_token = self.get_access_token()

    def scrape_one(self, url):
        """
        Scrape les données d'une URL spécifique de France Travail.
        
        :param url: L'URL à scraper.
        :return: Un dictionnaire contenant les données scrapées ou None en cas d'erreur.
        """
        try:
            # Faire une requête à l'URL
            print(f"Scraping France Travail URL: {url}")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Lève une exception pour les codes d'état HTTP non valides

            # Parser le contenu HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Extraire les données pertinentes
            job_title = soup.find("h1").text.strip() if soup.find("h1") else "No Title"
            job_description = soup.find("div", class_="description").text.strip() if soup.find("div", class_="description") else "No Description"
            company = soup.find("span", class_="company-name").text.strip() if soup.find("span", class_="company-name") else "No Company"
            location = soup.find("span", class_="job-location").text.strip() if soup.find("span", class_="job-location") else "No Location"

            return {
                "title": job_title,
                "company": company,
                "location": location,
                "description": job_description,
                "url": url
            }
        except requests.RequestException as e:
            print(f"Erreur lors du scraping de {url}: {e}")
            return None

    def get_access_token(self):
        """
        Récupère le token d'accès pour l'API Pôle Emploi.
        
        :return: Le token d'accès ou None en cas d'erreur.
        """
        payload = {
            "grant_type": "client_credentials",
            "client_id": "PAR_sise_6ecb7de16380e8802b4565918fcd2dab184e5916e58cba3b4ba4e09a9d124064",
            "client_secret": "fdd7ac75d36925e84f2fcbe0ed7cecf9619d01553708c4ac58f2c648e6bf3927",
            "scope": "api_offresdemploiv2 o2dsoffre"
        }
        try:
            response = requests.post("https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire", data=payload)
            response.raise_for_status()
            return response.json().get("access_token")
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération du token d'accès: {e}")
            return None

    def scrap_many(self, keyword, location=None, limit=5):
        """
        Récupère les offres d'emploi via l'API Pôle Emploi.
        
        :param keyword: Le mot-clé pour la recherche.
        :param location: Le code postal ou la localisation (optionnel).
        :param limit: Le nombre maximum de résultats à retourner.
        :return: Une liste d'offres d'emploi.
        """
        url = "https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "motsCles": keyword,
            "lieuTravail.codePostal": location,
            "range": f"0-{limit-1}"  # Nombre d'offres à récupérer
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json().get("resultats", [])
        except requests.RequestException as e:
            print(f"Erreur lors de la récupération des offres d'emploi: {e}")
            return []

    def display_offers(self, offers):
        """
        Affiche les offres d'emploi dans un format lisible.
        
        :param offers: Une liste d'offres d'emploi.
        """
        for offer in offers:
            titre = offer.get("intitule", "N/A")
            entreprise = offer.get("entreprise", {}).get("nom", "N/A")
            contrat = offer.get("typeContrat", "N/A")
            localisation = offer.get("lieuTravail", {}).get("libelle", "N/A")
            description = offer.get("description", "N/A")

            print("=" * 50)
            print(f"Titre : {titre}")
            print(f"Entreprise : {entreprise}")
            print(f"Contrat : {contrat}")
            print(f"Localisation : {localisation}")
            print(f"Description :\n{description}")

# # Exemple d'utilisation
# if __name__ == "__main__":
#     scraper = ScrapingFrancetravail()
#     offers = scraper.scrap_many("développeur", "75001", limit=3)
#     scraper.display_offers(offers)