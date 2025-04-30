import requests
from bs4 import BeautifulSoup
import os
import csv
from notion_client import Client
from datetime import datetime

# Initialisation de l'API Notion
notion = Client(auth="ton-token-d-integration")

# ID de ta base de données Notion
database_id = "ton-database-id"

# URL du site de scraping
url = "https://remoteok.io/remote-marketing-jobs"
headers = {'User-Agent': 'Mozilla/5.0'}

# Récupérer les données de la page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Créer un dossier avec la date du jour
today = datetime.today().strftime('%Y-%m-%d')
folder_name = f"scraped_jobs/{today}"
os.makedirs(folder_name, exist_ok=True)

# Ouvrir le fichier CSV dans le dossier du jour
csv_file = os.path.join(folder_name, 'jobs.csv')

jobs = soup.find_all('tr', class_='job')

# Sauvegarder les jobs dans un fichier CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Offre', 'Entreprise', 'URL', 'Date de publication'])  # L'ordre des colonnes dans le CSV
    
    for job in jobs:
        try:
            title = job.find('h2').text.strip()
            link = "https://remoteok.io" + job.find('a', class_='preventLink')['href']
            company = job.find('a', class_='companyLink')  # Chercher l'entreprise
            company_name = company.text.strip() if company else "Non spécifiée"  # Si l'entreprise n'est pas spécifiée

            # Ajouter les données dans le CSV
            writer.writerow([title, company_name, link, today])

            # Ajouter chaque job dans Notion
            notion.pages.create(
                parent={"database_id": database_id},
                properties={
                    "Offre": {  # Colonne "Offre"
                        "title": [
                            {
                                "text": {
                                    "content": title
                                }
                            }
                        ]
                    },
                    "Entreprise": {  # Colonne "Entreprise"
                        "rich_text": [
                            {
                                "text": {
                                    "content": company_name
                                }
                            }
                        ]
                    },
                    "URL": {  # Colonne "URL"
                        "url": link
                    },
                    "Date de publication": {  # Colonne "Date de publication"
                        "date": {
                            "start": today
                        }
                    }
                }
            )
        except Exception as e:
            print(f"Erreur en traitant cette offre : {e}")
            continue

print(f"✅ Les offres ont été sauvegardées dans {csv_file} et ajoutées à Notion.")
