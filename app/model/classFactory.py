import requests  # Pour faire des requêtes HTTP
from bs4 import BeautifulSoup  # Pour parser le HTML
from urllib.parse import urljoin  # Pour gérer les URLs relatives et absolues
from .classFrancetravail import ScrapingFrancetravail  # Import de la classe ScrapingFrancetravail

class ScrapingFactory:
    """
    Classe pour gérer le scraping sur plusieurs domaines.
    """

    # Liste des domaines supportés
    domains = [
        "francetravail.fr",
    ]

    def __init__(self):
        """
        Initialise la classe ScrapingFactory.
        """
        pass

    def url_check_in_domain(self, url):
        """
        Vérifie si l'URL donnée appartient à l'un des domaines supportés.
        
        :param url: L'URL à vérifier.
        :return: True si l'URL est supportée, False sinon.
        """
        for domain in self.domains:
            if domain in url:
                return True
        return False

    def scrap_one(self, url):
        """
        Scrape les données d'une URL spécifique.
        
        :param url: L'URL à scraper.
        :return: Les données scrapées ou None si l'URL n'est pas supportée.
        """
        if not self.url_check_in_domain(url):
            print(f"URL {url} n'est pas supportée.")
            return None

        # Utiliser le scraper approprié en fonction du domaine
        if "francetravail.fr" in url:
            scraper = ScrapingFrancetravail()
        else:
            print(f"Aucun scraper disponible pour l'URL {url}.")
            return None

        return scraper.scrape_one(url)

    def scrap_many(self, keyword, location=None, limit=5):
        """
        Scrape plusieurs offres d'emploi en fonction d'un mot-clé.
        
        :param keyword: Le mot-clé pour la recherche.
        :param location: La localisation (optionnelle).
        :param limit: Le nombre maximum de résultats à retourner.
        :return: Une liste d'offres d'emploi scrapées.
        """
        if not keyword:
            print("Un mot-clé est requis.")
            return []

        # Utiliser le scraper France Travail pour cet exemple
        scraper = ScrapingFrancetravail()
        return scraper.scrap_many(keyword, location, limit)

# # Exemple d'utilisation
# if __name__ == "__main__":
#     factory = ScrapingFactory()

#     # Scraping d'une seule URL
#     url = "https://www.francetravail.fr/offre-emploi"
#     scraped_data = factory.scrap_one(url)
#     if scraped_data:
#         print("Données scrapées :", scraped_data)

#     # Scraping de plusieurs offres d'emploi
#     keyword = "développeur"
#     offers = factory.scrap_many(keyword, location="75001", limit=3)
#     for offer in offers:
#         print("Offre :", offer)