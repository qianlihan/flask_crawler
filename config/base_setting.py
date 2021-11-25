# -*- coding: utf-8 -*-

DEBUG = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"
SECRET_KEY = "123456waterloo"


AUTH_COOKIE_NAME = "movie"
DEBUG_TB_INTERCEPT_REDIRECTS = False
DOMAIN = {
    "www": "http://127.0.0.1:5000"
}
