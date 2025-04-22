from enum import Enum

class _Video:
    TAG = 'i'
    ATTRS = {
        'class': 'tgme_widget_message_video_thumb',
    }
    URL_ATTR = 'style'

class _Photo:
    TAG = 'a'
    ATTRS = {
        'class': 'tgme_widget_message_photo_wrap',
    }
    URL_ATTR = 'style'

class _Views:
    TAG = 'span'
    ATTRS = {
        'class': 'tgme_widget_message_views',
    }

class _DateTime:
    TAG = 'time'
    DATETIME_ATTR = 'datetime'

class _Caption:
    TAG = 'div'
    ATTRS = {
        'class': 'tgme_widget_message_text js-message_text',
        'dir': 'auto',
    }

class _Main:
    TAG = 'div'
    ATTRS = {
        'class': 'tgme_widget_message_wrap js-widget_message_wrap',
    }

class _Link:
    TAG = 'div'
    ATTRS = {
        'class': 'tgme_widget_message text_not_supported_wrap js-widget_message',
    }
    LINK_ATTR = 'data-post'

class _Message:
    MAIN = _Main
    LINK = _Link
    CAPTION = _Caption
    _DATETIME = _DateTime
    VIEWS = _Views
    PHOTO = _Photo

class Tg:
    URL = 'https://t.me/s/'
    MESSAGE_ID_SEARCH_PARAM = 'before'
    MESSAGE = _Message


if __name__ == '__main__':
    print(Tg.URL.value)