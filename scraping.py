import requests
from bs4 import BeautifulSoup

url = "https://remoteok.com/remote-growth-jobs"

headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

jobs = soup.find_all('tr', class_='job')
for job in jobs:
    try:
        title = job.find('h2').text.strip()
        link = "https://remoteok.io" + job.find('a', class_='preventLink')['href']
        print(f"{title}\n{link}\n{'-'*50}")
    except:
        continue
