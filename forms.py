from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FileField, DecimalField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

class ProductForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    category = SelectField('Категория', choices=[('Игры', 'Игры'), ('Сервисы', 'Сервисы')], validators=[DataRequired()])
    description = TextAreaField('Описание', validators=[DataRequired()])
    price = DecimalField('Цена', validators=[DataRequired()])
    submit = SubmitField('Добавить товар')

class AvatarForm(FlaskForm):
    avatar = FileField('Аватар', validators=[DataRequired()])
    submit = SubmitField('Загрузить')
