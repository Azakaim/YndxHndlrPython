import random
from typing import Optional
import re
from Interfaces import IConcreteResponder
from SpintaxGenerator import ISpintaxGen


class PatternResponder(IConcreteResponder):
    responses_5_star: list[str]
    responses_4_star: list[str]
    responses_4bad_rev: list[str]
    spin: Optional[ISpintaxGen]

    def _responses(self, client_name=None, grade=None):
        result_response = ""
        if grade == 5:
            result_response = str(self.spin.spintax_generator(self.responses_5_star[0]))
        elif grade == 4:
            result_response = str(self.spin.spintax_generator(self.responses_4_star[0]))
        elif grade == 3:
            result_response = str(self.spin.spintax_generator(self.responses_4bad_rev[0]))
        text = re.split(r'[!.]', result_response)
        if client_name != "" and client_name is not None:
            return (text[0] + f", {client_name}" + random.choice(['.', '!']) +
                    ''.join([part + random.choice(['.', '!']) for part in text[1:] if part.strip()]))
        else:
            return result_response

    def response(self, **kwargs) -> str:
        switcher = {
            5: self._responses,
            4: self._responses,
            3: self._responses,
        }
        func_switcher = switcher.get(kwargs.get('grade')) if kwargs.get('grade') else ""
        if func_switcher:
            client_name = kwargs.get('name_client')
            grade = kwargs.get('grade')
            return func_switcher(client_name=client_name, grade=grade)
        else:
            return ""


class GPTResponder(IConcreteResponder):
    def response(self, **kwargs) -> str:
        return f"Hello, {kwargs.get('client_name')}! I will soon be created :)"
