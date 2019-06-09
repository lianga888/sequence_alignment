import configparser

from lib.app import app

config = configparser.ConfigParser()
config.read("config.ini")

if __name__ == "__main__":
    app.run(port=config["DEFAULT"]["PORT"])
