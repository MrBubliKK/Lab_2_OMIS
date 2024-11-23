from utils.database import connect_db
from typing import List, Optional, Tuple


class Report:
    def __init__(self, name: str, info: str, user_id: int, created_at: Optional[str] = None, report_id: Optional[int] = None):
        self.id = report_id
        self.user_id = user_id
        self.name = name
        self.info = info
        self.created_at = created_at
        self._user_info = None

    def save_to_db(self) -> None:
        """Сохраняет отчет в базу данных."""
        with connect_db() as conn:
            cursor = conn.cursor()
            if self.id is None:
                # Если отчета еще нет в БД, выполняем INSERT
                cursor.execute('''
                    INSERT INTO reports (user_id, name, info, created_at)
                    VALUES (?, ?, ?, DATE('now'))
                ''', (self.user_id, self.name, self.info))
                self.id = cursor.lastrowid  # Получаем ID добавленного отчета
                self.created_at = cursor.execute('SELECT DATE("now")').fetchone()[0]  # Получаем текущую дату
            else:
                # Если отчет уже существует, выполняем UPDATE
                cursor.execute('''
                    UPDATE reports
                    SET name = ?, info = ?, user_id = ?
                    WHERE id = ?
                ''', (self.name, self.info, self.user_id, self.id))
            conn.commit()

    @staticmethod
    def get_by_id(report_id: int) -> Optional["Report"]:
        """Получает отчет из базы данных по его ID."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, user_id, name, info, created_at FROM reports WHERE id = ?', (report_id,))
            row = cursor.fetchone()
            if row:
                return Report(name=row[2], info=row[3], user_id=row[1], created_at=row[4], report_id=row[0])
            return None

    @staticmethod
    def get_all_reports() -> List["Report"]:
        """Возвращает все отчеты из базы данных."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, user_id, name, info, created_at FROM reports ORDER BY created_at DESC')
            rows = cursor.fetchall()
            return [
                Report(name=row[2], info=row[3], user_id=row[1], created_at=row[4], report_id=row[0])
                for row in rows
            ]

    @staticmethod
    def get_reports_by_user(user_id: int) -> List["Report"]:
        """Возвращает все отчеты, созданные определенным пользователем."""
        with connect_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, user_id, name, info, created_at
                FROM reports
                WHERE user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
            rows = cursor.fetchall()
            return [
                Report(name=row[2], info=row[3], user_id=row[1], created_at=row[4], report_id=row[0])
                for row in rows
            ]

    def delete_from_db(self) -> None:
        """Удаляет отчет из базы данных."""
        if self.id:
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM reports WHERE id = ?', (self.id,))
                conn.commit()

    def get_user_info(self) -> Optional[Tuple[str, str]]:
        """
        Возвращает информацию о пользователе, связанном с отчетом (логин и должность).
        Кэширует результат для повышения производительности.
        """
        if self._user_info is None:  # Проверяем, есть ли уже кэшированные данные
            with connect_db() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT login, role FROM users WHERE id = ?', (self.user_id,))
                self._user_info = cursor.fetchone()
        return self._user_info

    @property
    def user_info(self) -> Optional[Tuple[str, str]]:
        """Свойство для получения информации о пользователе."""
        return self.get_user_info()
