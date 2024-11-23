from flask import session, flash, redirect, url_for, current_app
from app.models.user import User
import os
import uuid  # Для генерации уникальных имен файлов

class AuthController:
    @staticmethod
    def allowed_file(filename):
        """Проверяем разрешенный формат файла."""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

    def register(self, username, role, login, password, birthdate, avatar_file=None):
        """Регистрация нового пользователя."""
        avatar_filename = "default_avatar.png"  # Устанавливаем аватар по умолчанию
        if avatar_file and self.allowed_file(avatar_file.filename):
            # Генерируем уникальное имя для файла
            ext = avatar_file.filename.rsplit('.', 1)[1].lower()
            avatar_filename = f"{uuid.uuid4().hex}.{ext}"
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], avatar_filename)
            avatar_file.save(upload_path)

        # Создаем пользователя с сохраненным аватаром
        new_user = User(
            username=username,
            role=role,
            login=login,
            password=password,
            birthdate=birthdate,
            avatar=avatar_filename
        )
        new_user.save_to_db()
        flash("Пользователь успешно зарегистрирован.", "success")

    def login(self, login, password):
        """Авторизация пользователя."""
        user = User.authenticate(login, password)
        if user:
            session['user_id'] = user.id  # Сохраняем user_id в сессии
            return user
        else:
            flash("Неверный логин или пароль.", "danger")
            return None

    @staticmethod
    def logout():
        """Выход пользователя из системы."""
        session.pop('user_id', None)  # Удаляем user_id из сессии
        flash("Вы успешно вышли из системы", "info")

    @staticmethod
    def get_user_by_id(user_id):
        """Получение пользователя по ID."""
        return User.get_by_id(user_id)  # Здесь используется метод модели User
