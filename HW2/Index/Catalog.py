import pickle
from os.path import join
from Mapper import mappings_path


# CLASS CATALOG
class Catalog( object ):

    def __init__(self, name):
        self.name = name
        self.values = {}


    @classmethod
    def fromFile(self, path):
        d = readFrom(path)
        key = d.keys()[0]
        return d[key]


    def add(self, key, value):
        self.values[key] = value


    def delete(self, key):
        del self.values[key]


    def get_offsets(self, key):
        return self.values[key]


    def get(self):
        return self.values


    def __str__(self):
        return str(self.values)


# Module Functions
def write(c, folder):
    folder_path = folder + '/' + 'catalogfile'
    path = join(mappings_path, folder_path)
    with open(path, 'w') as f:
        pickle.dump(c, f)


def readFrom(folder):
    folder_path = join(mappings_path, folder)
    path = join(folder_path, 'catalogfile')
    with open(path, 'r') as f:
        return pickle.load(f)
