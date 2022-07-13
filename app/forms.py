from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField, RadioField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    """
    Форма входа в систему с 4 полями.
    """
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить')
    submit = SubmitField('Войти')


class UploadForm(FlaskForm):
    """
    Форма загрузки файла с 2 полями.
    """
    visible = BooleanField('Показывать файл')
    description = StringField('Описание файла')


class RatingForm(FlaskForm):
    """
    Форма оценки файла.
    """
    rating_plus = SubmitField('+1')
    rating_minus = SubmitField('-1')
    download = SubmitField('Скачать') # Попытка прикрутить загрузку


class RegistrationForm(FlaskForm):
    """
    Форма регистрации с проверками имени пользователя и адреса электронной почты.
    """
    username = StringField('Логин', validators=[DataRequired()])
    email = StringField('Почта', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password2 = PasswordField(
        'Повторите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Используйте другое имя пользователя')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Используйте другой адрес электронной почты')


