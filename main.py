from getpass import getpass
from upload_photo import get_to_copy
from upload_photo import get_album_select
from pprint import pprint

if __name__ == '__main__':
    # name_user = input('ID VK user: ')       # Запрос ID пользователя
    # token_yandex = getpass('Токен Яндекс: ')
    album_ids = {
        '1': 'wall',
        '2': 'profile',
        '3': 'saved',
        '4': 'album_user'
    }
    name_user = 'haritonova_love'
    token_yandex = 'AQAAAAACeEDqAADLW_r2MRLqXEoYhzq0WLwtM9o'
    choice_user = input(f'Какой альбом выбрать\n'
                        f'1| -- фото стены\n'
                        f'2| -- фото профиля\n'
                        f'3| -- сохраненные фото\n'
                        f'4| -- альбомы\n')
    if choice_user in '123':
        # pprint(album_ids[choice_user])
        try:
            num_photos = int(input('Количество фото (по умолчанию 5): '))
        except ValueError:
            num_photos = 5
        try:
            get_to_copy(name_user, token_yandex, num_photos, album_ids[choice_user])  # Вызов функции
        except TypeError:
            print('ACCESS DENIED')
    elif choice_user in '4':
        try:
            pprint(get_album_select(name_user))
        except TypeError:
            print('ACCESS DENIED')
        try:
            user_album_id = int(input('ID album: '))
            num_photos = int(input('Количество фото (по умолчанию 5): '))
            get_to_copy(name_user, token_yandex, num_photos, user_album_id)
        except ValueError:
            num_photos = 5
            user_album_id = 'profile'
            get_to_copy(name_user, token_yandex, num_photos, user_album_id)
        except TypeError:
            print('ACCESS DENIED')
    else:
        print('Invalid input')
