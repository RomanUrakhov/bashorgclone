from app import app
from posts.blueprint import posts

# ргеистрация блюпринта
# первый аргумент -- экземпляр класса blueprint (содердится в переменной posts)
app.register_blueprint(posts, url_prefix='/')

if __name__ == '__main__':
    app.run()
