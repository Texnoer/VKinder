from random import randrange
import requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from tokens import bot_token
from tokens import user_token
import json
from pprint import pprint

from data_base import check_id_user
token_u = user_token
token_b = bot_token


class Bot_Vkontakte:

    def __init__(self):
        self.vk = vk_api.VkApi(token=token_b)
        self.longpoll = VkLongPoll(self.vk)

    def write_msg(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})

    def communication(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                user = self.vk.method("users.get", {"user_ids": event.user_id})
                fullname = user[0]['first_name'] + ' ' + user[0]['last_name']
                if event.to_me:
                    request = event.text.lower()
                    if request == "старт":
                        self.write_msg(event.user_id, f"Ничего не нашёл.. пока..\n {fullname}, сори..")
                    elif request == "пока":
                        self.write_msg(event.user_id, "Пока((")
                    else:
                        self.write_msg(event.user_id, f"Привет, {fullname}!\n Давай начнём поиски пары! \nНапиши 'Старт'")


class Search_people:

    url = 'https://api.vk.com/method/'

    def __init__(self, age=None, gender=0, city=None, status=None):
        self.list_skipped = []
        self.token = token_u
        self.age = age
        self.gender = gender
        self.city = city
        self.status = status


    def search_user(self):
        users_url = self.url + 'users.search'
        users_params = {
            'access_token': self.token,
            'v': '5.126',
            'age_from': self.age,
            'age_to': self.age,
            'status': self.status,
            'sex': self.gender,
            'count': 1000,
            'hometown': self.city,
            'has_photo': 1,
            'fields': 'screen_name'
        }
        response = requests.get(users_url, params=users_params)
        result = response.json()
        if response in result:
            self.list_users = result['response']['items']
            return self.list_users
        # f = Search_people().search_user()
        # pprint(f)


    def get_photos(self, user_id):
        foto_url = self.url + 'photos.get'
        foto_params = {
            'access_token': self.token,
            'v': '5.126',
            'owner_id': user_id,
            'album_id': 'profile',
            'extended': True,
            'photo_sizes': True
        }
        photos = requests.get(foto_url, params=foto_params)
        return photos.json().get('response', {}).get('items', [])


    def get_largest(self, size_dict):
        """Функция ищет наибольший размер картинки"""
        if size_dict['width'] >= size_dict['height']:
            return size_dict['width']
        else:
            return size_dict['height']

    def sizes_max(self, photos):
        """Цикл поиска фото наибольшей популярности"""
        self.list_photo = []
        for photo in photos:
            sizes = photo['sizes']
            max_size = max(sizes, key=self.get_largest)['url']
            type_photo = max(sizes, key=self.get_largest)['type']
            self.list_photo.append({'url': max_size, 'likes': photo['likes']['count'] + photo['comments']['count'], 'type': type_photo})
        self.sort_photo = sorted(self.list_photo, key=lambda x: x['popular'], reverse=True)[:3]
        print(self.sort_photo)
        return self.sort_photo


    def user_profile(self, list_users):
        global user
        check_photo = {}
        check_database = 0
        while 'response' not in check_photo or check_database != True:
            if len(list_users) != 0:
                user = list_users.pop(0)
                check_database = check_id_user(user['id'])
                check_photo = self.get_photos(user['id'])
            else:
                break
        self.user_profile_dict = {}
        self.user_profile_dict['name'] = user['first_name']
        self.user_profile_dict['last_name'] = user['last_name']
        self.user_profile_dict['id'] = user['id']
        self.user_profile_dict['url'] = 'https://vk.com/id' + str(user['id'])
        self.user_profile_dict['photo'] = self.sizes_max(check_photo)
        return self.user_profile_dict

    def download_list_skipped(self, user):
        self.list_skipped.append(user)

    def get_user(self):
        if len(self.list_users) != 0:
            return self.user_profile(self.list_users)
        elif len(self.list_skipped) != 0:
            return self.list_skipped.pop(0)
        elif len(self.list_users) == 0 and len(self.list_skipped) == 0:
            return None

# if __name__ == '__main__':
#     Bot_Vkontakte().communication()