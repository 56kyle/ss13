
import re

class Mappable:
    prefix = ''

    def __init__(self, text: str):
        super().__init__()
        self.text = text
        path_regex = r'/?' + self.prefix + r'[^{]+'
        path_match = re.search(path_regex, self.text)
        self.path = path_match.group(0) if path_match else ''

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'{self.__class__.__name__}(\'{self.text}\')'

    def __eq__(self, other):
        if isinstance(other, Mappable):
            return self.path == other.path
        else:
            return self.path.split('/')[-1] == other.split('/')[-1]


class Area(Mappable):
    prefix = 'area'


class Turf(Mappable):
    prefix = 'turf'


class Obj(Mappable):
    prefix = 'obj'

