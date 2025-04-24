from typing import Union, Literal

from enums.tg import Tg


Targets = [attr for attr in dir(Tg.MESSAGE) + dir(Tg.CHANNEL) if not (attr.startswith('__') and attr.endswith('__'))]

# python doesnt allow literal types to be dinamically computed
# fuck python
# im going to stick to ts

if  __name__ == '__main__':
    print([1, 2, 3] + [4, 5])