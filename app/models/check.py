import sqlite3
from app.models.settings import Settings
from datetime import datetime


class Check:
    """Класс, представляющий проверку оборудования."""

    def __init__(self, name, settings, date=None, display_date=True, display_count=True, display_fallability=True):
        self.name = name
        self.settings = settings
        self.date = date or datetime.now().strftime("%Y-%m-%d")
        self.display_date = display_date
        self.display_count = display_count
        self.display_fallability = display_fallability

    def getView(self):
        """Метод для отображения данных проверки."""
        print(f"Название проверки: {self.name}")
        print(f"Дата выполнения: {self.date}")
        print(f"Количество проверок: {self.settings.count}")
        print(f"Вероятность отказа: {self.settings.fallability}")
        print("Тесты:")
        for test in self.settings.tests:
            print(f"  Название: {test.name}")
            print(f"    Вес: {test.weight}")
            print(f"    Размер: {test.size}")
            print(f"    Температура: {test.temperature}")

    def changeView(self, new_name):
        """Изменение имени проверки."""
        self.name = new_name
        print(f"Имя проверки изменено на: {self.name}")

    def setNewSettings(self, count, fallability, tests):
        """Обновление настроек проверки с новыми значениями."""
        self.settings.count = int(count)
        self.settings.fallability = float(fallability)
        self.settings.tests = tests
        print("Настройки проверки обновлены.")

    def save(self, equipment_id):
        """Сохранение проверки в базу данных."""
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()

        print("Данные для сохранения:", self.name, equipment_id, self.date, self.settings.count,
              self.settings.fallability)

        cursor.execute("""
            INSERT INTO checks (name, equipment_id, info, date, count, fallability)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            self.name,
            equipment_id,  # Используем переданный equipment_id
            "Информация о тесте",  # Можно заменить на данные из self.settings
            self.date,
            self.settings.count,
            self.settings.fallability
        ))

        conn.commit()
        conn.close()


    @staticmethod
    def load_for_device(equipment_id):
        """Загрузка всех проверок для определенного устройства из базы данных."""
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT name, equipment_id, info, date, count, fallability FROM checks WHERE equipment_id = ?",
                       (equipment_id,))
        checks = cursor.fetchall()
        conn.close()

        # Создаем экземпляры Check для каждой записи, загруженной из базы данных
        return [
            Check(
                name=name,
                settings=Settings(count=count, fallability=fallability, tests=[]),  # Укажите тесты, если они есть
                date=date
            )
            for name, equipment_id, info, date, count, fallability in checks
        ]

    @classmethod
    def load_all(cls):
        """Загрузить все проверки из базы данных с учетом отображения критериев."""
        checks = []
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()

        # Извлекаем все проверки из базы данных, включая флаги отображения
        cursor.execute("""
            SELECT name, info, date, count, fallability, display_date, display_count, display_fallability
            FROM checks
        """)
        rows = cursor.fetchall()

        conn.close()

        # Для каждой строки создаем объект Check
        for row in rows:
            name, info, date, count, fallability, display_date, display_count, display_fallability = row

            # Создаем настройки для проверки, используя значения из базы данных
            settings = Settings(count=count, fallability=fallability, tests=[])  # Укажите тесты, если они есть

            # Создаем объект Check и добавляем его в список
            check = cls(
                name=name,
                settings=settings,
                date=date,
                display_date=display_date,
                display_count=display_count,
                display_fallability=display_fallability
            )
            checks.append(check)

        return checks

    def calculate_average_percentage(self, equipment, tests):
        """Вычисляет средний процент результатов тестов для указанного оборудования."""
        if not tests:
            raise ValueError("Список тестов пуст. Невозможно вычислить средний процент.")

        total_percentage = 0
        for test in tests:
            percentages = test.calculate_percentages(equipment)
            total_percentage += percentages["result_precentage"]

        average_percentage = total_percentage / len(tests)
        return average_percentage

    @staticmethod
    def update_display_for_all(criterion, display_value):
        """Метод для обновления отображения одного критерия для всех проверок."""
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()

        if criterion == 'date':
            cursor.execute("""UPDATE checks SET display_date = ?""", (display_value,))
        elif criterion == 'count':
            cursor.execute("""UPDATE checks SET display_count = ?""", (display_value,))
        elif criterion == 'fallability':
            cursor.execute("""UPDATE checks SET display_fallability = ?""", (display_value,))

        conn.commit()
        conn.close()