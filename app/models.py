from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    """
    Таблица с данными о пользователе.
    id: уникальный id
    username: имя пользователя
    email: адрес элекстронной почты.
    password_hash: хеширование пароля
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    """ Загрузка пользователя """
    return User.query.get(int(id))


class Files(db.Model):
    """
    Таблица с данными о пользователе.
    id: уникальный id файла.
    filename: имя файла.
    description: описание файла, заданное при загрузке.
    data: содержимое файла в бинарном формате.
    visibility: видимость с булевым значением.
    user_id: id пользователя, загрузившего файл.
    rating: значение рейтинга файла, по умолчанию = 0
    """
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    description = db.Column(db.String(150))
    data = db.Column(db.LargeBinary)
    visibility = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    rating = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Files {}>'.format(self.body)