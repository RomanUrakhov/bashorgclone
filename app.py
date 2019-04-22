from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

# Механизм миграции для внесения изменения в БД после изменения кода (z.b добавили новый аттрибут)
# такие параметры нужны т.к механизму миграции необходимо знать о текущей
# версии приложения и состоянии БД
migrate = Migrate(app, db)
manager = Manager(app)
# регистрация команды для консоли для миграции
manager.add_command('db', MigrateCommand)

