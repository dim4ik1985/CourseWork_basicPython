from getpass import getpass
from upload_photo import get_to_copy
from pprint import pprint

if __name__ == '__main__':
    name_user = input('ID VK user: ')       # Запрос ID пользователя
    token_yandex = getpass('Токен Яндекс: ')
    try:
        num_photos = int(input('Количество фото (по умолчанию 5): '))
    except ValueError:
        num_photos = 5
    get_to_copy(name_user, token_yandex, num_photos)  # Вызов функции
