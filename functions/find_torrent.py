import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

def search_torrent(query):
    # Заменяем пробелы на '+' для URL
    search_url = f"http://rutor.info/search/0/0/000/2/{query.replace(' ', '+')}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'
    }

    # Получаем HTML-код страницы с результатами поиска
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return None  # Если запрос не удался

    # Парсинг HTML с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    # Ищем все результаты с классом, характерным для раздач
    for row in soup.find_all('tr', class_='gai'):  # Класс 'gai' для ссылок на руторе
        try:
            # Находим заголовок и ссылку на магнит
            title = row.find_all('a')[2].text  # Третий тег <a> содержит заголовок раздачи
            magnet_link = row.find('a', title="магнет")['href']
            seeds = int(row.find_all('td')[2].text)  # Количество сидов во второй ячейке

            # Добавляем результат в список
            results.append({
                'title': title,
                'magnet_link': magnet_link,
                'seeds': seeds
            })
        except (IndexError, ValueError, TypeError):
            continue  # Пропускаем, если произошла ошибка парсинга

    # Сортируем раздачи по количеству сидов и возвращаем лучшую
    if results:
        best_torrent = max(results, key=lambda x: x['seeds'])
        return best_torrent
    else:
        return None
    
def find_torrent(update: Update, context: CallbackContext) -> None:
    query = " ".join(context.args)
    best_torrent = search_torrent(query)
    
    if best_torrent:
        update.message.reply_text(
            f"Найден торрент: {best_torrent['title']}\nСиды: {best_torrent['seeds']}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Скачать", callback_data=f"download_{best_torrent['magnet_link']}")]
            ])
        )
    else:
        update.message.reply_text("Не удалось найти торренты по вашему запросу.")