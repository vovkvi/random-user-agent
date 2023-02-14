#!/usr/bin/env python3
# coding : utf-8
'''
Простой класс для генерации случайного юзер агента с использованием
сайта http://useragentstring.com

(c) Vitalii Vovk, 2022
'''
import random
import re
import ssl
import urllib.request


class RandomUserAgent(str):


    USERAGENTSTRING_URL = 'http://useragentstring.com/pages/useragentstring.php'
    BROWSERS = ['Chrome','Firefox','Edge','Opera','Mozilla','Safari']


    def __new__(cls, timeout:int = 10):
        '''
        Создает новый экземпляр объекта класса RandomUserAgent

        :param:
            timeout (int) : таймаут ожидания ответа от сервера

        :return:
            str : строка со случайным юзер агентом
        '''
        html = ''
        brsr = RandomUserAgent.BROWSERS[random.randint(0, len(RandomUserAgent.BROWSERS)-1)]
        uri = f'{RandomUserAgent.USERAGENTSTRING_URL}?name={brsr}'
        try:
            req = urllib.request.Request(uri, headers={'user-agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ssl.create_default_context(), timeout=timeout) as conn:
                html = conn.read().decode()
        except urllib.error.HTTPError as e:
            print(f'[-] HTTP Error: {e.reason}')
            return
        except urllib.error.URLError as e:
            print(f'[-] URL Error: {e.reason}')
            return
        except ValueError as e:
            print(f'[-] Value Error: {e}')
            return
        li = re.findall(r'<li>(.+?)</li>', html, re.UNICODE)
        agent_list = [re.search(r">(.+?)</a>", e.strip())[1] for e in li]
        return str.__new__(cls, agent_list[random.randint(0, len(agent_list)-1)])
