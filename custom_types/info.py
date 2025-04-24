from enums.tg import Tg


Infos = [attr for attr in dir(Tg) if not (attr.startswith('__') and attr.endswith('__'))]