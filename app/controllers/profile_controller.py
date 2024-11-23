import uuid
from werkzeug.utils import secure_filename
import os
from flask import current_app


class ProfileController:
    def __init__(self, user):
        self.user = user

    def update_profile(self, updated_data, avatar=None):
        """Обновляет данные пользователя в базе данных, если они изменились."""
        changes = False

        # Обновляем только те поля, которые изменились и не пустые
        if updated_data.get('username') and updated_data['username'] != self.user.username:
            self.user.username = updated_data['username']
            changes = True

        if updated_data.get('role') and updated_data['role'] != self.user.role:
            self.user.role = updated_data['role']
            changes = True

        if updated_data.get('login') != '' and updated_data.get('login') != self.user.login:
            self.user.login = updated_data['login']
            changes = True

        if updated_data.get('password') != '' and updated_data.get('password') != self.user.password:
            self.user.password = updated_data['password']
            changes = True

        if updated_data.get('birthdate') != '' and updated_data.get('birthdate') != self.user.birthdate:
            self.user.birthdate = updated_data['birthdate']
            changes = True

        print(avatar)

        # Проверка на наличие аватара и генерация уникального имени для файла
        if avatar:
            avatar_filename = self._generate_avatar_filename(avatar)
            self.user.avatar = avatar_filename
            changes = True

        if changes:
            self.user.update_in_db()

    def _allowed_file(self, filename):
        """Проверяет, допустимо ли расширение файла."""
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    def _generate_avatar_filename(self, avatar_file):
        """Генерирует уникальное имя для файла аватара с использованием uuid."""
        if avatar_file and self._allowed_file(avatar_file.filename):
            ext = avatar_file.filename.rsplit('.', 1)[1].lower()
            avatar_filename = f"{uuid.uuid4().hex}.{ext}"  # Генерация уникального имени с uuid
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], avatar_filename)
            avatar_file.save(upload_path)  # Сохранение файла на сервере
            return avatar_filename
        return None

