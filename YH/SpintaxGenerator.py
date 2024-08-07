import random
import re
from abc import ABC


class ISpintaxGen(ABC):
    def spintax_generator(self, text: str):
        pass


class SpintaxGen(ISpintaxGen):
    def spintax_generator(self, text: str):
        while True:
            text, n = re.subn(r'\{([^{}]*)\}', lambda m: random.choice(m.group(1).split('|')), text)
            if n == 0:
                break
        return text
