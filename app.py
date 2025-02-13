from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_mail import Mail, Message
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from models import db, User, Product, Order, MessageModel, Review
from forms import RegistrationForm, LoginForm, ProductForm, AvatarForm

# Инициализация приложения
app = Flask(__name__)
app.config.from_object(Config)

# Подключение расширений
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)
admin = Admin(app, name='Admin Panel', template_mode='bootstrap3')

# Добавление моделей в админ-панель
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(MessageModel, db.session))
admin.add_view(ModelView(Review, db.session))

# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Главная страница
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Регистрация успешна!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

# Авторизация
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Вы успешно вошли в систему.')
            return redirect(url_for('index'))
        else:
            flash('Неверный email или пароль.')
    return render_template('login.html', form=form)

# Выход
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.')
    return redirect(url_for('index'))

# Профиль
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = AvatarForm()
    if form.validate_on_submit():
        file = form.avatar.data
        filename = file.filename
        file.save(f'static/avatars/{filename}')
        current_user.avatar = filename
        db.session.commit()
        flash('Аватар обновлен')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)

# Каталог товаров
@app.route('/catalog')
def catalog():
    products = Product.query.all()
    return render_template('catalog.html', products=products)

# Добавление товара
@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if form.validate_on_submit():
        new_product = Product(
            title=form.title.data,
            category=form.category.data,
            description=form.description.data,
            price=form.price.data,
            seller_id=current_user.id
        )
        db.session.add(new_product)
        db.session.commit()
        flash('Товар добавлен')
        return redirect(url_for('catalog'))
    return render_template('add_product.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
