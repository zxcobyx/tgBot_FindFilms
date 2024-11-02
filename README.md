# tgBot_FindFilms

For start bot:
1. Write terminal - sudo systemctl start transmission-daemon
2. Write terminal - sudo systemctl status transmission-daemon
3. python3 main.py

For drop bot:
1. Write terminal - sudo systemctl stop transmission-daemon

Add requirements.txt:
1. pipreqs ./ --ignore .venv --force --encoding=utf-8

TODO:
1. Сделать поиск и загрузку magnet-ссылок на Rutor
2. Сделать аутентификацию, либо использовать куки с текущим сеансом для стабильной загрузки торрентов. 
3. Сделать поиск и загрузку magnet-ссылок на Rutracker. 
4. Сделать автоматическое добавление .torrent в приложение загрузки торрент-файлов. 
5. Сделать возможность проверки статуса загрузки, в котором будет название торрента, скорость загрузки файла
6. Добавить возможность паузы и остановки загрузки торрент файлов. 
7. Добавить возможность просмотра всех медиа - файлов на сервере, а так же возможность их удаления. 
8. Прописать доступ к боту через админ панель (писать/отвечать только админ id) 