# models/operator.py
import sqlite3
from app.models.user import User
from app.models.equipment import Equipment
from app.models.result import Result
from typing import List


class Operator(User):
    def __init__(self, username, role, login, password, birthdate, avatar):
        super().__init__(username=username, role=role, login=login, password=password, birthdate=birthdate,
                         avatar=avatar)
        print("username ", username)
        self.equipments: List[Equipment] = []  # Список оборудования
        self.result: Result = None  # Последний результат тестирования

    def setEquipment(self, equipment: Equipment):
        """Добавить оборудование в список оператора и сохранить в базу данных."""
        self.equipments.append(equipment)
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO devices (operator_id, device_name) VALUES (?, ?)", (self.id, equipment.name))
        conn.commit()
        conn.close()

    def getEquipment(self) -> List[Equipment]:
        """Возвращает список оборудования оператора."""
        return self.equipments

    def load_devices(self):
        """Загрузить устройства из базы данных."""
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT device_name FROM devices WHERE operator_id=?", (self.id,))
        devices = cursor.fetchall()
        conn.close()
        # Инициализируем Equipment на основе загруженных данных
        self.equipments = [
            Equipment(name=device[0], quality=0, speed=0, efficiency=0, price=0, safety=0, condition=True) for device in
            devices]

    def runTests(self):
        """Запуск тестов для всего оборудования оператора."""
        if not self.equipments:
            return "Нет оборудования для тестирования."

        results = []
        for equipment in self.equipments:
            result = self.createResult(equipment)
            self.save_test_result(equipment.name, result)  # Сохраняем результат в базу данных
            results.append(result)
        return results

    def createResult(self, equipment: Equipment) -> Result:
        """Создаёт и возвращает результат теста для оборудования."""
        # Псевдозначения для примера
        weight = 10.0
        size = 5.0
        temperature = 22.0
        testtype = "Проверка работоспособности"
        checks = equipment.getSettings()  # Получаем текущие настройки как проверку

        # Создаём новый результат
        self.result = Result(weight=weight, size=size, temperature=temperature, testtype=testtype, checks=checks)
        self.test_results.append(self.result)
        return self.result

    def checkResult(self) -> str:
        """Возвращает последнюю информацию о результате теста."""
        if self.result:
            return f"Последний результат тестирования: Вес - {self.result.getWeight()}, Размер - {self.result.getSize()}, Температура - {self.result.getTemperature()}, Тип теста - {self.result.getTestType()}"
        return "Результатов тестирования пока нет."

    def save_test_result(self, device, result):
        """Сохранить результат теста в базе данных."""
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO test_results (operator_id, device_name, weight, size, temperature, testtype)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (self.id, device, result.getWeight(), result.getSize(), result.getTemperature(), result.getTestType()))
        conn.commit()
        conn.close()
