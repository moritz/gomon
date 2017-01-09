from os import environ
import configparser

def config():
    c = configparser.ConfigParser()
    c.read(environ.get('GOMON_CONFIG_FILE', 'gomon.ini'))
    return c
