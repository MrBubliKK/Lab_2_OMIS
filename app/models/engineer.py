from app.models.test import Test
from app.models.report import Report
from app.models.user import User


class Engineer(User):
    def __init__(self, user_id, name, email, reports=None):
        super().__init__(user_id, name, email)
        self.reports = reports if reports else []

    def runTests(self, equipments):
        """Запуск тестов для всего оборудования оператора."""
        if not equipments:
            return "Нет оборудования для тестирования."

        results = []
        for equipment in equipments:
            Test.calculate_percentages(equipment)


    def checkResult(self, test_id):
        # Пример логики проверки
        test_result = self.get_test_result_by_id(test_id)  # Получаем результат теста из базы данных
        if not test_result:
            return False
        elif test_result['status'] == "Passed":
            return True
        else:
            return False

    def setSettings(self, equipment, settings):
        """
        Устанавливает настройки для указанного оборудования.
        """
        if not equipment:
            return "Оборудование не найдено."

        try:
            equipment.setNewSettings(
                weight=settings.get("weight", equipment.settings["weight"]),
                size=settings.get("size", equipment.settings["size"]),
                temperature=settings.get("temperature", equipment.settings["temperature"])
            )
            equipment.save()  # Сохраняем изменения в базу данных
            return f"Настройки для оборудования {equipment.name} обновлены: {equipment.getSettings()}."
        except Exception as e:
            return f"Ошибка при обновлении настроек: {e}"

    def viewReports(self):
        if not self.reports:
            return "Отчеты отсутствуют."

        report_list = []
        for report in self.reports:
            report_info = f"ID: {report.report_id}, Title: {report.title}, Summary: {report.content[:50]}..."
            report_list.append(report_info)
        return "\n".join(report_list)

    def analyzeReport(self, report_id, keywords):
        report = next((r for r in self.reports if r.report_id == report_id), None)
        if not report:
            return False

        issues_found = [word for word in keywords if word in report.content.lower()]

        if issues_found:
            return True
        else:
            return False

    def createReport(self, title, content):
        report_id = len(self.reports) + 1
        new_report = Report(report_id, title, content)
        self.reports.append(new_report)