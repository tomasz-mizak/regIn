from dotenv import dotenv_values
from os.path import isfile

class Config:

    def __init__(self, path = '.env'):
        if isfile(path):
            self.config = dotenv_values(path)
        else:
            raise FileNotFoundError(f"config.py - enviroment file not exists on path {path}.")

    def get(self, key):
        try:
            return self.config[key]
        except KeyError as exception:
            print(f"KeyError: No declared {key}.")
            return False