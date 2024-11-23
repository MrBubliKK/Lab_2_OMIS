import os


class Config:
    # Устанавливаем путь для загрузки файлов, используя переданный root_path из create_app
    UPLOAD_FOLDER = 'D:\\University work\\5 sem\\OMIS\\Lab 2\\uploads'  # Изначально None, будет инициализировано в create_app
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Можете добавить другие конфигурации по вашему усмотрению
    SECRET_KEY = 'b315de23bc6ceeaeafec3b8d42d8c6fd193f77a3e95eb75f'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
