**Сервис для отправки сообщении в телеграм**

Для получения API_ID и API_HASH нужно зайти на https://my.telegram.org/apps

Для создания сессии используем 
>python3 start.py

После создаем контейнер
>docker-compose -p telethon-app build

и запускаем
>docker-compose -p telethon-app up -d