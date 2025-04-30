import requests
from bs4 import BeautifulSoup
import csv

url = "https://remoteok.io/remote-marketing-jobs"
headers = {'User-Agent': 'Mozilla/5.0'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

jobs = soup.find_all('tr', class_='job')

# Ouvrir le fichier CSV en écriture
with open('jobs.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Link'])  # En-têtes

    for job in jobs:
        try:
            title = job.find('h2').text.strip()
            link = "https://remoteok.io" + job.find('a', class_='preventLink')['href']
            writer.writerow([title, link])
        except:
            continue

print("✅ Les offres ont été sauvegardées dans jobs.csv")
