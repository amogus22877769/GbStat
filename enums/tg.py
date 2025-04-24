from enum import Enum
from datetime import datetime
from re import compile
from typing import Generator

from bs4 import BeautifulSoup

class _Info:
    TAG: str
    ATTRS: dict[str: str] = {}
    ATTR: str
    METHOD = '__getitem__'
    def PARSE(string: str) -> any:
        return string

class _Sticker(_Info):
    TAG = 'i'
    ATTRS = {
        compile(r'tgme_widget_message_sticker js-sticker_image'),
    }
    ATTR = 'data-webp'

class _Video(_Info):
    TAG = 'video'
    ATTR = 'src'

class _Photo(_Info):
    TAG = 'a'
    ATTRS = {
        'class': compile(r'tgme_widget_message_photo_wrap'),
    }
    ATTR = 'style'
    def PARSE(style: str) -> str:
        if len(style.split("'")) != 1:
            return style.split("'")[1]
        return style.split('"')[1]
    

class _Views(_Info):
    TAG = 'span'
    ATTRS = {
        'class': 'tgme_widget_message_views',
    }
    ATTR = 'string'
    METHOD = '__getattribute__'

class _DateTime(_Info):
    TAG = 'time'
    ATTRS = {
        'class': 'time',
    }
    ATTR = 'datetime'
    def PARSE(time: str) -> datetime:
        return datetime.fromisoformat(time)

class _Caption(_Info):
    TAG = 'div'
    ATTRS = {
        'class': 'tgme_widget_message_text js-message_text',
        'dir': 'auto',
    }
    ATTR = 'strings'
    METHOD = '__getattribute__'
    def PARSE(strings: Generator[str, None, None]):
        string: str = ''
        for substring in strings:
            string += substring
        return string

class _Main(_Info):
    TAG = 'div'
    ATTRS = {
        'class': 'tgme_widget_message_wrap js-widget_message_wrap',
    }

class _Id(_Info):
    TAG = 'div'
    ATTRS = {
        'class': compile(r'tgme_widget_message text_not_supported_wrap'),
    }
    ATTR = 'data-post'
    def PARSE(link: str) -> int:
        return int(link.split('/')[1])

class _Message:
    MAIN = _Main
    ID = _Id
    CAPTION = _Caption
    DATETIME = _DateTime
    VIEWS = _Views
    PHOTO = _Photo
    VIDEO = _Video
    STICKER = _Sticker

class _Title(_Info):
    TAG = 'title'
    ATTR = 'string'
    METHOD = '__getattribute__'
    def PARSE(string: str) -> str:
        return string[:-12]

class _Description(_Info):
    TAG = 'div'
    ATTRS = {
        'class': 'tgme_channel_info_description',
    }
    ATTR = 'strings'
    METHOD = '__getattribute__'
    def PARSE(strings: Generator[str, None, None]):
        string: str = ''
        for substring in strings:
            string += substring
        return string

class _Subscribers(_Info):
    TAG = 'span'
    ATTRS = {
        'class': 'counter_value'
    }
    ATTR = 'string'
    METHOD = '__getattribute__'

class _Channel:
    TITLE = _Title
    DESCRIPTION = _Description
    SUBSCRIBERS = _Subscribers

class Tg:
    URL = 'https://t.me/s/'
    MESSAGE_ID_SEARCH_PARAM = 'before'
    MESSAGE = _Message
    CHANNEL = _Channel


if __name__ == '__main__':
    print("width:449px;background-image:url('https://cdn4.cdn-telegram.org/file/qE7VEhm0Ei1zQwjRoWe28JLj9wTSoUgg18plAG102oVvukcVxesKg4iOAyV_-XkO2cN9JV1qgmiB206eQMBdL9o0tp3ZrHQvbLIroAwJ65QOjt_CnECQJ7Elq4n7lTUnASln4x9j2ECtR8M_I4CsvYQbE_xj0iZq26qDn-3CNhdOcKbTlmrkz1dpuuxy0lSHdQJ4tuju4VHJ42YPTjfKFvGXe7uOW5e_dVDWsslq4HYzRp5AU_xWqHW8CCegEvGsjMaAv54qXjBSSV6ymWukdKWBuql1XvMhIFxSpbRKOsnqPXWXyEaCnMfQbe6KRadRGAOnNy_knnFH5DMXuCPoXA.jpg')"
          .split("'")[1])
    print('left: 292px; top: 0px; width: 145px; height: 217px; margin-right: 0px; margin-bottom: 0px; background-image: url("https://cdn4.cdn-telegram.org/file/MIT3QXirewoQMLg3-V_uNzWSp8Xz2uZ2c1VmcQKYN5PPOurf3Y67WUIILdB3U8csErPM8kMQy-2Y3fR9I5K2iLc02woNsB45m9sQlwAaydL851_N4IsQlxeA9JsUww9AwxgkrQy-u_VrJELNydzqIPQCzmi8OhMVpY4UW30tJXtgvN4hOjyUDIzrEf5U0_pnOKjIS5xi1o9kyN-6jex_cglwN_Ick84UNZFUMKtInQOiXVblGk8tSmLMigkdI54R7yL1MId-_HlbEygOPA9cy-zZ41ccBbWcbuSUIZ0ucFK9wQEA133S9iblOG04ugcB3bhMOeprPNpujQN79vqSmg.jpg");'
          .split('"')[1])
    print('a'.split('.'))
    print('amogus22877769🏀♿️ – Telegram'[:-12])
    print(BeautifulSoup('<p>1</p><p>2</p>').find('p'))
    
