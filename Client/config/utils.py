import configparser
import datetime as dt


def load_config(path: str) -> dict:
    config = configparser.ConfigParser()
    config.read(path)

    return config

def client_print(s: str):
    print(f"[{dt.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}] " + s)