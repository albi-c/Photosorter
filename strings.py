import os

class Strings:
    def __init__(self, stringfile):
        self.stringfile = stringfile

        with open(stringfile) as f:
            data = f.read()
        
        self.data = {}

        for line in data.splitlines():
            if not line or line.startswith("#"):
                continue

            key, value = line.split("=", 1)
            key = key.strip()
            self.data[key] = eval(f'"{value}"')
    def __getitem__(self, key):
        return self.data[key]
    def __setitem__(self, key, value):
        self.data[key] = value
    def __delitem__(self, key):
        del self.data[key]
