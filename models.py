from app import db
import datetime
import re


def slugify(post_title):
    pattern = r'[^\w+]'
    # 1 арг. -- что ищем, 2 арг. -- на что заменяем
    return re.sub(pattern, '-', post_title)


# Класс отвечающий за хранение постов
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    # человекопонятный уникальный идентификатор
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    rating = db.Column(db.Integer, default=0)

    # *args -- список поизиционных аргументов (кот. можем передать к контруктор)
    # **kwargs -- словарь именнованных аргументов (пушо kw=key word)
    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        self.generate_slug()

    def generate_slug(self):
        if self.title:
            st = datetime.datetime.timestamp(datetime.datetime.now())
            self.slug = slugify(self.title + str(st))

    def __repr__(self):
        return '<Post id: {}, title: {}>'.format(self.id, self.title)
