from app.models.test import Test

class Settings:
    """Класс для хранения настроек проверки."""
    def __init__(self, count, fallability, tests=None):
        self.count = int(count)
        self.fallability = float(fallability)
        self.tests = tests if tests is not None else []

    def add_test(self, test):
        """Добавить новый тест к настройкам."""
        if isinstance(test, Test):
            self.tests.append(test)
        else:
            raise ValueError("Добавляемый элемент должен быть экземпляром класса Test")

    def getCount(self):
        return self.count

    def getFallability(self):
        return self.fallability
