# coding: utf-8
from application import db


class Movie(db.Model):
    __tablename__ = 'movie'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False,
                     server_default=db.FetchedValue())
    genre = db.Column(db.String(100), nullable=False,
                      server_default=db.FetchedValue())
    cover_pic = db.Column(db.String(300), nullable=False,
                          server_default=db.FetchedValue())
    pics = db.Column(db.String(1000), nullable=False,
                     server_default=db.FetchedValue())
    url = db.Column(db.String(300), nullable=False,
                    server_default=db.FetchedValue())
    description = db.Column(db.Text, nullable=False)
    hash = db.Column(db.String(32), nullable=False,
                     unique=True, server_default=db.FetchedValue())
    release_date = db.Column(db.DateTime, nullable=True,
                             server_default=db.FetchedValue())
    source = db.Column(db.String(20), nullable=False,
                       server_default=db.FetchedValue())
    length = db.Column(db.String(20), nullable=False,
                       server_default=db.FetchedValue())
    gross = db.Column(db.Integer, nullable=False,
                      server_default=db.FetchedValue())
    update_time = db.Column(db.DateTime, nullable=False,
                            server_default=db.FetchedValue())
    create_time = db.Column(db.DateTime, nullable=False,
                            server_default=db.FetchedValue())

    def __init__(self, **items):
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
