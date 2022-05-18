
import numpy as np
import os
import re

from PIL import Image

from ss13.mappable import Area, Turf, Obj


class Map:
    def __init__(self, file):
        text = file.read()
        file.close()
        self.data = self.parse(text)
        self.coords = self.get_coords(text)
        #print(self.coords)

    @staticmethod
    def make_lists(match: re.Match):
        group_2 = match.group(2).lstrip("\n")
        return f'"{match.group(1)}" = [{group_2}]'

    def parse(self, text):
        data = {}
        new = re.sub(r'"(\w\w\w)"\s?=\s?\(([^)]*)\)', self.make_lists, text, flags=re.DOTALL)
        groups = re.findall(r'"(\w\w\w)"\s?=\s?\[([^]]*)\]', new, flags=re.DOTALL)
        for code, objects in groups:
            turf_match = re.search(r'/turf[^},]*}?', objects)
            turf = Turf(turf_match.group(0)) if turf_match else None
            area_match = re.search(r'/area[^},]*}?', objects)
            area = Area(area_match.group(0)) if area_match else None
            objects = [Obj(obj) for obj in re.findall(r'/obj[^},]*}?', objects)]
            data[code] = {'turf': turf, 'area': area, 'objects': objects}
        return data

    @staticmethod
    def get_coords(text):
        coords = []
        column_matches = re.findall(r'(\(\d+ ?,\d+ ?,\d+\)) ?= ?{"([^"}]+)"}', text, flags=re.DOTALL)
        for coor, contents in column_matches:
            x = eval(coor)[0]
            coords.append([])
            rows = contents.strip('\n').split('\n')
            for y, code in enumerate(rows):
                coords[x-1].insert(0, code)
        return np.array(coords).T

    def get_zipped_coords(self):
        for y, row in enumerate(self.coords):
            for x, val in enumerate(row):
                yield (x, y), val

    def get_coor(self, x, y):
        return self.coords[y-1][x-1]

    def get_turf(self, x, y):
        return self.data[self.get_coor(x, y)]['turf']

    def get_area(self, x, y):
        print(self.data[self.get_coor(x, y)])
        return self.data[self.get_coor(x, y)]['area']

    def get_objects(self, x, y):
        return self.data[self.get_coor(x, y)]['objects']

    def get_img(self):
        img = Image.new('RGB', self.coords.shape)
        for y, row in enumerate(reversed(self.coords)):
            for x, val in enumerate(row):
                img.putpixel((x, y), tuple([int(ord(v)) for v in val]))
        return img

    def find_codes(self, turf=None, area=None, obj=None):
        valid_codes = []
        for code, contents in self.data.items():
            valid = True
            if turf:
                valid = valid and contents.get('turf') == turf
            if area:
                valid = valid and contents.get('area') == area
            if obj:
                valid = valid and obj in contents.get('objects')
            if valid:
                valid_codes.append(code)
        return valid_codes

    def find(self, turf=None, area=None, obj=None):
        valid_codes = self.find_codes(turf, area, obj)
        print(valid_codes)
        for coor, code in self.get_zipped_coords():
            if code in valid_codes:
                yield coor


if __name__ == '__main__':
    map = Map(open('../data/cogmap.dmm', 'r'))
    img = Image.new('RGB', map.coords.shape)
    for coor in map.find(obj='yellow'):
        print(f'{coor[0]},{coor[1]}')
        img.putpixel((coor[0], map.coords.shape[1] - coor[1]), (255, 0, 0))
    img.show()







