from typing import List
from app.models.check import Check
from datetime import datetime

class Result:
    def __init__(self, weight: float, size: float, temperature: float, testtype: str, checks: List[Check]):
        self.weight = weight
        self.size = size
        self.temperature = temperature
        self.testtype = testtype
        self.date = datetime.now()  # Устанавливаем дату на момент создания экземпляра
        self.checks = checks  # Список объектов Check, связанных с этим результатом

    # Методы доступа к атрибутам класса
    def getWeight(self) -> float:
        return self.weight

    def getSize(self) -> float:
        return self.size

    def getTemperature(self) -> float:
        return self.temperature

    def getDate(self) -> datetime:
        return self.date

    def getTestType(self) -> str:
        return self.testtype

    def getChecks(self) -> List[Check]:
        return self.checks
