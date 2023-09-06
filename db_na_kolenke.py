from peewee import *

db = SqliteDatabase('chats.db')


class Message(Model):
    name = CharField()
    text = TextField()

    class Meta:
        database = db
