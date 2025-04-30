import requests
from bs4 import BeautifulSoup
import csv
import os
from datetime import datetime

# URL du site de scraping
url = "https://remoteok.io/remote-marketing-jobs"
headers = {'User-Agent': 'Mozilla/5.0'}

# Récupérer les données de la page
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# Créer un dossier avec la date du jour (format: YYYY-MM-DD)
today = datetime.today().strftime('%Y-%m-%d')
folder_name = f"scraped_jobs/{today}"
os.makedirs(folder_name, exist_ok=True)

# Ouvrir le fichier CSV dans le dossier du jour
csv_file = os.path.join(folder_name, 'jobs.csv')

jobs = soup.find_all('tr', class_='job')

# Sauvegarder dans un fichier CSV
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link'])  # En-têtes
    
    for job in jobs:
        try:
            title = job.find('h2').text.strip()
            link = "https://remoteok.io" + job.find('a', class_='preventLink')['href']
            writer.writerow([title, link])
        except:
            continue

print(f"✅ Les offres ont été sauvegardées dans {csv_file}")
