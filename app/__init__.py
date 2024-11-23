from flask import Flask, send_from_directory
from config.config import Config
from config.extensions import db, login_manager  # Импортируем из нового модуля
from app.models.user import User
import os

from app.routes import routes  # Импортируем маршруты

def create_app():
    app = Flask(__name__, static_folder='static')

    # Конфигурация приложения
    app.config['SECRET_KEY'] = 'b315de23bc6ceeaeafec3b8d42d8c6fd193f77a3e95eb75f'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Путь для загрузки файлов
    app.config['UPLOAD_FOLDER'] = 'D:\\University work\\5 sem\\OMIS\\Lab 2\\uploads'

    # Задаем путь для загрузки файлов в Config
    Config.UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)

    app.config.from_object(Config)

    # Устанавливаем метод загрузки пользователя
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))

    login_manager.login_view = 'authenticate'
    login_manager.login_message = "Пожалуйста, войдите в систему, чтобы получить доступ к этой странице."

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # Регистрируем маршруты
    app.register_blueprint(routes)  # <-- Добавьте эту строку

    return app
