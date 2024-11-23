from flask_login import UserMixin
from config.extensions import db  # Импортируем db из extensions
from utils.database import connect_db


class User(db.Model, UserMixin):  # Наследуем от UserMixin для поддержки Flask-Login
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.Date)
    avatar = db.Column(db.String(255), default='default_avatar.png')

    def __init__(self, username=None, role=None, login=None, password=None, birthdate=None, avatar=None, id=None):
        self.id = id
        self.username = username
        self.role = role
        self.login = login
        self.password = password
        self.birthdate = birthdate
        self.avatar = avatar

    def save_to_db(self):
        """Сохраняет пользователя в базу данных."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(''' 
                INSERT INTO users (username, role, login, password, birthdate, avatar)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (self.username, self.role, self.login, self.password, self.birthdate, self.avatar))
            conn.commit()
            self.id = cursor.lastrowid  # Устанавливаем id после сохранения

    def update_in_db(self):
        """Обновляет данные пользователя в базе данных."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users
                SET username = ?, role = ?, login = ?, password = ?, birthdate = ?, avatar = ?
                WHERE id = ?
            ''', (self.username, self.role, self.login, self.password, self.birthdate, self.avatar, self.id))
            conn.commit()

    @staticmethod
    def authenticate(login, password):
        """Проверяет логин и пароль пользователя для авторизации."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, username, role, login, password, birthdate, avatar
                FROM users WHERE login = ? AND password = ?
            ''', (login, password))
            user_data = cursor.fetchone()
            if user_data:
                return User(
                    id=user_data[0],
                    username=user_data[1],
                    role=user_data[2],
                    login=user_data[3],
                    password=user_data[4],
                    birthdate=user_data[5],
                    avatar=user_data[6]
                )
            else:
                return None

    @staticmethod
    def get_by_id(user_id):
        """Получает пользователя по его ID из базы данных."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute(''' 
                SELECT id, username, role, login, password, birthdate, avatar 
                FROM users WHERE id = ? 
            ''', (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(
                    id=user_data[0],
                    username=user_data[1],
                    role=user_data[2],
                    login=user_data[3],
                    password=user_data[4],
                    birthdate=user_data[5],
                    avatar=user_data[6]
                )
            return None

    @classmethod
    def get_by_login(cls, login):
        return cls.query.filter_by(login=login).first()
