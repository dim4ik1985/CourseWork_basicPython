import requests
import time
import json
from tqdm import tqdm


with open('token_vk.txt', 'r') as file_vk:
    token_vk = file_vk.read().strip()


class VkBackup:
    host_vk = 'https://api.vk.com/method/'

    def __init__(self, ids):
        self.ids = ids
        self.param_vk = {
            'access_token': token_vk,
            'v': '5.131'
        }

    def __user_id(self):
        user_info_url = self.host_vk + 'users.get'
        user_info_param = {
            'user_ids': self.ids,
        }
        res = requests.get(user_info_url, params={**self.param_vk, **user_info_param}).json()
        return res['response'][0]['id']

    def account_app_permissions(self):
        url = self.host_vk + 'account.getAppPermissions'
        params = {
            'user_id': self.__user_id()
        }
        response = requests.get(url, params={**self.param_vk, **params}).json()
        return response

    def get_photo_list(self, count=5, album_id='profile'):
        photo_list_url = self.host_vk + 'photos.get'
        photo_list_param = {
            'owner_id': self.__user_id(),
            'album_id': album_id,
            'extended': '1',
            'photo_sizes': '1',
            'count': count
        }
        response = requests.get(photo_list_url,
                                params={**self.param_vk, **photo_list_param}).json().get('response')
        return response

    def photos_albums(self):
        album_list_url = self.host_vk + 'photos.getAlbums'
        album_list_params = {
            'owner_id': self.__user_id(),
            'photo_sizes': '1'
        }
        response = requests.get(album_list_url, params={**self.param_vk, **album_list_params}).json().get('response')
        return response

    def get_query_to_copy(self, count=5, album='profile'):
        user_photo = self.get_photo_list(count, album)['items']
        return user_photo


class YaUploader:
    host_ya = 'https://cloud-api.yandex.net'
    info_dict = {
        "file_name": f'',
        "size": None
    }
    to_join = []

    def __init__(self, token):
        self.token = token
        self.header = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    def check_path(self):
        """
        Проверка на валидность токена
        :return: status code
        """
        headers = {
            'Accept': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        url = f'{self.host_ya}/v1/disk'
        res = requests.get(url, headers=headers)
        return res.status_code

    def __create_folder(self, path_folder, album_id):
        url = f'{self.host_ya}/v1/disk/resources'
        params = {
            'path': path_folder,
            'fields': 'href'
        }
        response = requests.get(url, params=params, headers=self.header).status_code
        if response == 404:
            requests.put(url, params=params, headers=self.header)
        else:
            params = {
                'path': f'{path_folder}/{album_id}',
                'fields': 'href'
            }
            requests.put(url, params=params, headers=self.header)

    def upload(self, path, name_file, url_photo, size, album_id):
        """
        Запрос загрузки файлов
        :param album_id:
        :param path: Путь созданной папки для загрузки файлов
        :param name_file: Название файла
        :param url_photo: url файла
        :param size: Размер файла
        :return: Возврат json-файла с информацией по файлам
        """
        url = f'{self.host_ya}/v1/disk/resources/upload'
        self.__create_folder(path, album_id)
        params = {
            'path': f'{path}/{album_id}/{name_file}.jpg',
            'url': url_photo,
        }
        requests.post(url, headers=self.header, params=params)
        self.info_dict['file_name'] = f'{name_file}.jpg'
        self.info_dict['size'] = size
        self.to_join.append(self.info_dict.copy())
        with open(f'{"info/"}load_{path}_{album_id}.json', 'w') as f:
            json.dump(self.to_join, f, ensure_ascii=False, indent=0)


def get_to_copy(ids, token, count, album_id='profile'):
    """
    Копирование файлов
    :param album_id:
    :param ids: ID VK user
    :param token: Token API Yandex
    :param count: Количество запросов для скачивания
    :return: Копирование файлов и результат копирования
    """
    user_vk = VkBackup(ids)
    disk_user = YaUploader(token)
    user_copy = user_vk.get_query_to_copy(count, album_id)
    check_counter = []
    if disk_user.check_path() == 200:
        for el in tqdm(user_copy):
            if el['likes']['count'] not in check_counter:
                disk_user.upload(ids, el['likes']['count'], el['sizes'][-1]['url'], el['sizes'][-1]['type'], album_id)
                check_counter.append(el['likes']['count'])
            else:
                disk_user.upload(ids, el['date'], el['sizes'][-1]['url'], el['sizes'][-1]['type'], album_id)
            time.sleep(.5)
        del check_counter
        print('Загрузка завершена')
    else:
        print(f'Код ошибки {disk_user.check_path()}')


def get_album_select(ids):
    user_vk = VkBackup(ids)
    album_dict = {
        'id': None,
        'title': None
    }
    to_album = []
    res = user_vk.photos_albums()
    for item in res['items']:
        if item['size'] != 0:
            album_dict['id'] = item['id']
            album_dict['title'] = item['title']
            to_album.append(album_dict.copy())
    return to_album
