import requests
from bs4 import BeautifulSoup

async def search_torrent_rutor(query):
    search_url = f"http://rutor.info/search/0/0/100/2/{query.replace(' ', '+')}"
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36' }

    print(search_url)

    response = requests.get(search_url, headers=headers)

    print(response)
   
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    count = 0

    for row in soup.find_all('tr', class_=['gai', 'tum']):
        try:
            # Извлечение магнитной ссылки
            magnet_link = row.find('a', href=lambda x: x and x.startswith('//d.rutor.info/download/'))['href']
            
            # Извлечение названия
            title = row.find('a', href=lambda x: x and x.startswith('/torrent/')).text.strip()
            
            # Извлечение количества сидов (по желанию)
            seeds = int(row.find_all('td')[-1].find('span', class_='green').text.strip().split()[0])

            # Извлечение ссылки на торрент
            link = row.find('a', href=lambda x: x and x.startswith('/torrent/'))['href']
            
            # Полный URL для ссылки на торрент
            torrent_url_long= f'https://rutor.info{link}'

            # Размер торрента
            size_cells = row.find_all('td', align='right')
            size_torrent = None
            for cell in size_cells:
                if 'GB' in cell.text or 'MB' in cell.text:
                    size_torrent = cell.text.strip()
                    break

            if size_torrent is None:
                size_torrent = "Размер неизвестен"

            results.append({
                'title': title,
                'magnet_link': magnet_link.replace('//', ''),
                'seeds': seeds,
                'link': torrent_url_long,
                'size': size_torrent
            })

            count += 1

        except (AttributeError, IndexError, ValueError, TypeError):
            continue

    if results:
        best_torrents = sorted(results, key=lambda x: x['seeds'], reverse=True)[:3]
            
        return best_torrents
    else:
        return None