import qbittorrentapi as qbt

# Создаем экземпляр клиента
client = qbt.Client(host='localhost:8080', username='admin', password='adminadmin')

async def add_torrent_by_url(_urls: list, new_name: str = None):
    """
    Загружает торрент из списка URL в qBittorrent.
    
    :param urls: Список URL-адресов торрент-файлов
    :return: Сообщение об успешной загрузке или об ошибке
    """
    try:
        print(_urls)

        result = client.torrents_add(urls=_urls, rename=new_name)
        print(f"Результат добавления торрента: {result}")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return None
    
async def add_torrent_by_url_wn(_urls: list):
    """
    Загружает торрент из списка URL в qBittorrent.
    
    :param urls: Список URL-адресов торрент-файлов
    :return: Сообщение об успешной загрузке или об ошибке
    """
    try:
        print(_urls)

        result = client.torrents_add(urls=_urls)
        print(f"Результат добавления торрента: {result}")
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")
        return None

def get_torrents_status():
    """
    Получает статус всех загружающихся торрентов.
    
    :return: Список словарей с информацией о прогрессе и скорости загрузки для каждого торрента
    """
    torrents_info = client.torrents_info(status_filter="all")  # Получаем информацию о всех торрентах
    active_torrents = []

    for torrent in torrents_info:
        active_torrents.append({
            "name": torrent.name,
            "progress": torrent.progress * 100
        })
    
    if active_torrents:
        return active_torrents
    else:
        print("Нет активных торрентов для загрузки.")
        return None