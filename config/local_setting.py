
from config.base_setting import *
#SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "mysql://root:Leonard2@127.0.0.1/movie_cat"

SECRET_KEY = "imooc123456"

DOMAIN = {
    "www": "http://127.0.0.1:5000"
}

RELEASE_PATH = "/Users/qianlihan/flask_project/release_version"
