import datetime

from mongoengine import *
class User(Document):
    email=StringField(required=True)
    password=StringField(max_length=50)
    name=StringField()
    image=ImageField(upload_to='./img/')

    def __str__(self):
        return self.email

# Create your models here.

class Article(Document):
    title = StringField(required=True,max_length=30)
    content = StringField(required=True)
    weather=StringField()
    author = StringField()
    date = DateTimeField(default=datetime.datetime.now)
    category = StringField(required=True)

    def __str__(self):
        return self.title

