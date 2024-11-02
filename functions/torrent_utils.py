import requests
import aiohttp
from urllib.parse import urljoin
from typing import Optional
from transmission_rpc import Client
from constants import TORRENT_FOLDER

# Инициализация реального клиента Transmission
transmission_client = Client(host='localhost', port=9091, username='transmission', password='YourName102')

async def download_torrent_file(url: str) -> Optional[bytes]:
    """
    Асинхронно загружает .torrent файл по указанному URL.
    
    :param url: URL торрент-файла
    :return: Содержимое торрент-файла или None в случае ошибки
    """
    # Добавляем протокол и домен, если их нет
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url.lstrip('/')
    
    print(url)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                else:
                    print(f"Ошибка при загрузке торрент-файла: HTTP статус {response.status}")
                    return None
    except aiohttp.ClientError as e:
        print(f"Ошибка при загрузке торрент-файла: {e}")
        return None

async def add_torrent(torrent_data: bytes):
    """
    Добавляет торрент в Transmission.
    
    :param torrent_data: Содержимое торрент-файла (bytes)
    :return: ID добавленного торрента
    """
    torrent = transmission_client.add_torrent(torrent_data, download_dir=TORRENT_FOLDER)
    return torrent.id

def get_torrent_status(torrent_id):
    """
    Получает статус торрента.
    
    :param torrent_id: ID торрента
    :return: Словарь с информацией о прогрессе и скорости загрузки
    """
    torrent = transmission_client.get_torrent(torrent_id)
    return {
        "progress": torrent.progress,
        "rateDownload": torrent.rate_download / 1000  # Конвертируем в кБ/с
    }