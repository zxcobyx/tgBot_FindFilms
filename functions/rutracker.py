import requests
from bs4 import BeautifulSoup

async def search_torrent_rutracker(query):
    search_url = f"http://rutracker.org/forum/tracker.php?nm={query.replace(' ', '+')}"
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36' }

    print(search_url)

    response = requests.get(search_url, headers=headers)

    print(response)
   
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    # print(soup)
    
    with open('outputRutracker.txt', 'w', encoding='utf-8') as file:
        file.write(str(soup))

    for row in soup.find_all('tr', class_='gai'):
        try:
            title = row.find_all('a')[2].text
            magnet_link = row.find('a', title="downgif")['href']
            seeds = int(row.find_all('td')[2].text)

            results.append({
                'title': title,
                'magnet_link': magnet_link,
                'seeds': seeds
            })
        except (IndexError, ValueError, TypeError):
            continue

    print(results)

    if results:
        best_torrent = max(results, key=lambda x: x['seeds'])
        return best_torrent
    else:
        return None