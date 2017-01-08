import configparser

def config():
    c = configparser.ConfigParser()
    c.read('gomon.ini')
    return c
