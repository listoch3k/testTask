from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, UploadForm, RatingForm
from app.models import User, Files


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """
    Заглавная страница. Включает в себя вызов формы для проставления рейтинга файла,
    отображение файлов с видимостью, выставленной на True при загрузке.
    :return: Рендер заглавной страницы, переменные для Jinja2.
    """
    form = RatingForm()
    files = Files.query.filter(Files.visibility == 1)
    """ Нереализованная функция. При POST запросе значение рейтинга файла увеличивается на 1.
    Не получилось реализовать оценку для конкретного файла. 
    if form.validate_on_submit() and form.rating_plus.data == '+1':
        for file in files:
            file.rating += 1
            db.session.commit()
            return redirect(url_for('index'))
    if form.validate_on_submit() and form.rating_minus.data == '-1':
        for file in files:
            file.rating += 1
            db.session.commit()
            return redirect(url_for('index'))
    """
    return render_template('index.html', title='Главная', files=files, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Страница входа в систему с проверками корректности данных.
    :return: Рендер страницы входа, переменные для Jinja2.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неправильное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Войти', form=form)


@app.route('/logout')
def logout():
    """
    Вызов метода выхода пользователя из системы.
    :return: Перенаправление на заглавную страницу.
    """
    logout_user()
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    """
    Страница ЛК пользователя. Если пользователь авторизован, отображает файлы, загруженные пользователем
    и форму загрузки файла с проверкой видимости.
    :return: Рендер страницы профиля и переменные для Jinja2 если пользователь авторизован, в противном
    случае редирект на заглавную страницу.
    """
    if current_user.is_authenticated:
        files = Files.query.filter(Files.user_id == current_user.get_id())
        form = UploadForm()
        return render_template('profile.html', files=files, form=form)
    else:
        redirect(url_for('index.html'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Страница регистрации. Реализованная при помощи FlaskForm.
    :return: Страница регистрации, переменные для Jinja2.
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Регистрация прошла успешно!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    """
    Форма загрузки файла, привязанная к странице профиля. При выполнении POST запроса файл, выбранный
    пользователем, загружается в таблицу Files.
    :return: Рендер страницы профиля, переменная для Jinja2.
    """
    form = UploadForm()
    if request.method == 'POST':
        file = request.files['file']
        upload = Files(filename=file.filename, data=file.read(), visibility=form.visible.data, user_id=current_user.get_id(),
                       description=form.description.data)
        db.session.add(upload)
        db.session.commit()
        flash('Файл успешно загружен!')
        return render_template('profile.html', form=form)

