from app.models.check import Check
from app.models.settings import Settings
from app.models.test import Test

class CheckController:
    def __init__(self, user_id):
        self.user_id = user_id

    def add_check(self, name, equipment_id, info, weight, size, temperature):
        # Создаем тесты с переданными показателями
        tests = [
            Test("Тест веса", weight, size, temperature)
        ]
        # Создаем настройки для проверки с количеством проверок и вероятностью отказа (например, по умолчанию)
        settings = Settings(count=1, fallability=0.1, tests=tests)
        # Создаем и сохраняем проверку
        check = Check(name=name, settings=settings)
        check.save(equipment_id)

    def get_all_checks(self):
        checks = Check.load_all()  # Предположительно этот метод возвращает все проверки
        return checks

    def calculate_average_percentage_for_check(self, check_name, equipment):
        """Вычисляет средний процент для проверки с указанным именем и оборудованием."""

        # Загрузка всех проверок
        checks = Check.load_all()

        # Поиск проверки по имени
        check = next((c for c in checks if c.name == check_name), None)
        if not check:
            return None

        # Вычисляем средний процент
        average_percentage = check.calculate_average_percentage(equipment)

        return average_percentage
