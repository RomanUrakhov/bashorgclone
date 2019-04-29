from app import db
import datetime
import re


def slugify(post_title):
    pattern = r'[^\w+]'
    # 1 арг. -- что ищем, 2 арг. -- на что заменяем
    return re.sub(pattern, '-', post_title)


post_tags = db.Table('post_tags',
                     db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                     )


# Класс отвечающий за хранение постов
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))
    # человекопонятный уникальный идентификатор
    slug = db.Column(db.String(140), unique=True)
    body = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.datetime.now())
    rating = db.Column(db.Integer, default=0)

    # параметр lazy='dynamic' говорит о том, что при обращении к свойству backref экземпляра класса Tag, мы получаем
    # объект класса BaseQuery, для чтобы чтобы можно было использовать его (у BaseQuery) специальные свойства/методы
    tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('relevant_posts', lazy='dynamic'))

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


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(100))

    def __init__(self, *args, **kwargs):
        super(Tag, self).__init__(*args, **kwargs)
        self.slug = slugify(self.name)

    def __repr__(self):
        return '<Tag id: {}, name: {}'.format(self.id, self.name)
