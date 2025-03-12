import requests  
from bs4 import BeautifulSoup
import requests


class ScrapingFrancetravail:
    # En-têtes pour imiter un vrai navigateur
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    CLIENT_ID = "PAR_sise_6ecb7de16380e8802b4565918fcd2dab184e5916e58cba3b4ba4e09a9d124064"
    CLIENT_SECRET = "fdd7ac75d36925e84f2fcbe0ed7cecf9619d01553708c4ac58f2c648e6bf3927"

    def __init__(self):
        self.base_url = "https://www.francetravail.fr"  # Base URL for France Travail
        self.access_token  = self.get_access_token()

    def scrapeOne(self, url):
        """
        Scrape data from a single France Travail URL.
        
        :param url: The URL to scrape.
        :return: Scraped data as a dictionary or None if an error occurs.
        """
        try:
            # Make a request to the URL
            print(f"Scraping France Travail URL: {url}")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise an error for bad status codes

            # Parse the HTML content
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract relevant data
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
            print(f"Error scraping {url}: {e}")
            return None

    def get_access_token(self):
        """
        Retrieve the access token for the Pôle Emploi API.
        
        :return: The access token.
        """
        cLIENT_ID = "PAR_sise_6ecb7de16380e8802b4565918fcd2dab184e5916e58cba3b4ba4e09a9d124064"
        cLIENT_SECRET = "fdd7ac75d36925e84f2fcbe0ed7cecf9619d01553708c4ac58f2c648e6bf3927"
        tOKEN_URL = "https://entreprise.pole-emploi.fr/connexion/oauth2/access_token?realm=/partenaire"
        
        payload = {
            "grant_type": "client_credentials",
            "client_id": cLIENT_ID,
            "client_secret": cLIENT_SECRET,
            "scope": "api_offresdemploiv2 o2dsoffre"
        }
        try:
            response = requests.post(tOKEN_URL, data=payload)
            response.raise_for_status()
            return response.json()["access_token"]
        except requests.RequestException as e:
            print(f"Error retrieving access token: {e}")
            return None

    def scrapMany(self, keyword, location=None, limit=5):
        """
        Fetch job offers from the Pôle Emploi API.
        
        :param access_token: The access token for the API.
        :param keyword: The keyword to search for.
        :param location: The postal code or location (optional).
        :param limit: The maximum number of results to return.
        :return: A list of job offers.
        """
        url = "https://api.pole-emploi.io/partenaire/offresdemploi/v2/offres/search"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        params = {
            "motsCles": keyword,
            "lieuTravail.codePostal": location,
            "range": f"0-{limit-1}"  # Number of offers to retrieve
        }

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json().get("resultats", [])
        except requests.RequestException as e:
            print(f"Error fetching job offers: {e}")
            return []

    def display_offers(self, offers):
        """
        Display job offers in a readable format.
        
        :param offers: A list of job offers.
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
