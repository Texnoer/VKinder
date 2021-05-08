from random import randrange
import requests

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from tokens import bot_token

token = bot_token

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        user = vk.method("users.get", {"user_ids": event.user_id})
        fullname = user[0]['first_name'] + ' ' + user[0]['last_name']
        if event.to_me:
            request = event.text.lower()
            if request == "старт":
                write_msg(event.user_id, f"Хай, {fullname}")
            elif request == "пока":
                write_msg(event.user_id, "Пока((")
            else:
                write_msg(event.user_id, f"Привет, {fullname}!\n Давай начнём поиски пары! \nНапиши 'Старт'")
