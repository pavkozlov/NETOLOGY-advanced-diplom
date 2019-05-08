# VKInder

Все слышали про известное приложение для знакомств - Tinder. Приложение предоставляет простой интерфейс для выбора понравившегося человека. Сейчас в Google Play более 100 миллионов установок. Используя данные из VK был сделан сервис намного лучше чем Tinder.

## Инструкция

1) Скачайте проект к себе на компьютер и установите все необходимые зависимости из файла reqirements.txt: `pip install -r requirements.txt`
2) Получите AccessToken от сайта vk.com с правами доступа _groups_
3) Введите AccessToken и ID пользователя для которого ищем пару в файл config.py (в AUTH_PARAMS)

    3.1) Если не указать данные там, и оставить **None**, при запуске в консольном режиме программа попросит их ввести
4) Полученный результат будет записан в базу данных MongoDB и JSON файл под названием **result.json**. Так же в базу данных будет записана информация о профиле, для которого ищем пару и все найденые люди, в возрасте 18-23 (Можно изменить диапазон в файле config.py, в разделе AUTH_PARAMS) года (по 1000 на каждый год), из этого же города, противоположного пола
5) У вас должна быть локально настроенная или удалённая система управления базами данных **MONGO DB** (параметры подключения задаются в файле config.py, в разделе DB_PARAMS)
6) Запустите из командной строки VKinder.py:
`python3 VKinder.py`
8) Логи работы программы можно посмотреть в файле _sample.log_
### О программе

Используя данные из VK я сделал сервис намного лучше чем Tinder. Сервис ищет людей, подходящих под условия, на основании информации о пользователе из VK:

    диапазон возраста
    пол
    общие группы
    расположение
    интересы
    музыка
    книги

У каждого критерия поиска есть свои веса. Задаются они в config.py, в разделе SEARCH_PARAMS. По умолчанию совпадение по общим группам важнее совпадения по книгам. Любимые книги важнее музыкальных предпочтений. Музыкальные предпочтения важнее интересов.

У тех людей, которые подошли по требованиям пользователю, получаем топ-3 популярных фотографии с аватара. Популярность определяется по количеству лайков.

### Требования

Установленный Python версии 3.*

## Тесты

Все модульные тесты находятся в папке **test**, и тестируют основные компоненты программы
