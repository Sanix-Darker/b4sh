import configparser

conf = configparser.RawConfigParser()
conf.read(r'config.txt')

DATABASE_HOST = conf.get("b4", "DATABASE_HOST")
DATABASE_NAME = conf.get("b4", "DATABASE_NAME")
