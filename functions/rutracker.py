import requests
from bs4 import BeautifulSoup
from rutracker_api import RutrackerApi
from rutracker_api.exceptions import AuthorizationException

from constants import USERNAME_RUTRACKER, PASSWORD_RUTRACKER

# # Функция для входа
# def login_rutracker():
#     login_url = "http://rutracker.org/forum/login.php"
#     session = requests.Session()
    
#     # Данные для входа
#     payload = {
#         'login_username': USERNAME_RUTRACKER,
#         'login_password': PASSWORD_RUTRACKER,
#         'redirect': 'forum/index.php'
#     }

#     # Выполнение входа
#     response = session.post(login_url, data=payload)

#     with open('responceText.txt', 'w', encoding='utf-8') as file:
#         file.write(str(response.text)) 
    
#     if response.status_code == 200 and USERNAME_RUTRACKER not in response.text:  # Проверка успешности входа  
#         return session
#     else:
#         print("Ошибка входа")
#         return None

# async def search_torrent_rutracker(query):
#     session = login_rutracker()
#     if not session:
#         return None

#     search_url = f"http://rutracker.org/forum/tracker.php?nm={query.replace(' ', '+')}"
#     headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36' }

#     print(search_url)

#     response = requests.get(search_url, headers=headers)

#     print(response)
   
#     if response.status_code != 200:
#         return None

#     soup = BeautifulSoup(response.text, 'html.parser')
#     results = []
#     # print(soup)

#     with open('outputRutracker.txt', 'w', encoding='utf-8') as file:
#         file.write(str(soup))

#     for row in soup.find_all('tr', class_='gai'):
#         try:
#             title = row.find_all('a')[2].text
#             magnet_link = row.find('a', title="downgif")['href']
#             seeds = int(row.find_all('td')[2].text)

#             results.append({
#                 'title': title,
#                 'magnet_link': magnet_link,
#                 'seeds': seeds
#             })
#         except (IndexError, ValueError, TypeError):
#             continue

#     print(results)

#     if results:
#         best_torrent = max(results, key=lambda x: x['seeds'])
#         return best_torrent
#     else:
#         return None

async def search_torrent_rutracker(query):
    # Создаем экземпляр API
    api = RutrackerApi()

    # Логин и пароль
    username = USERNAME_RUTRACKER
    password = PASSWORD_RUTRACKER

    # Вход в систему
    try:
        api.login(username, password)
        print("Успешный вход!")
    except AuthorizationException:
        print("Ошибка при входе: Неправильный логин или пароль.")
        return None
    except Exception as e:
        print(f"Ошибка при входе: {e}")
        return None

    # Выполнение поиска
    try:
        search_result = api.search(query)
        results = []

        for torrent in search_result['result']:
            results.append({
                'title': torrent.title,
                'magnet_link': torrent.magnet_link,
                'seeds': torrent.seeds
            })

        print(results)

        if results:
            best_torrent = max(results, key=lambda x: x['seeds'])
            return best_torrent
        else:
            return None

    except Exception as e:
        print(f"Ошибка при выполнении поиска: {e}")
        return None