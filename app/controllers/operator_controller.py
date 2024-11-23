# controllers/operator_controller.py
from app.models.operator import Operator
from app.models.equipment import Equipment


class OperatorController:
    def __init__(self, operator=None):
        self.operator = operator  # Сохраняем оператора, если передан

    def add_operator(self, username, role, login, password, birthdate, avatar):
        """Создать нового оператора и добавить его в систему."""
        operator = Operator(username, role, login, password, birthdate, avatar)
        operator.save()  # Предполагается, что есть метод save для User

    def add_equipment_to_operator(self, operator_id, equipment: Equipment):
        """Добавить оборудование оператору."""
        operator = Operator.load_by_id(operator_id)
        if operator:
            operator.setEquipment(equipment)


    def load_operator_equipment(self, operator_id):
        """Загрузить все оборудование оператора."""
        operator = Operator.load_by_id(operator_id)
        if operator:
            equipment = operator.getEquipment()


    def run_tests_for_operator(self, operator_id):
        """Запустить тесты для всего оборудования оператора."""
        operator = Operator.load_by_id(operator_id)
        if operator:
            results = operator.runTests()


    def check_last_test_result(self, operator_id):
        """Проверить последний результат теста оператора."""
        operator = Operator.load_by_id(operator_id)
        if operator:
            result = operator.checkResult()

