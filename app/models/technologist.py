from app.models.user import User
from app.models.equipment import Equipment


class Technologist(User):
    def __init__(self, user_id, name, email, data=None):
        super().__init__(user_id, name, email)
        self.data = data if data else []  # Список данных, связанных с технологом

    def getReportInfo(self, report_id):
        report = next((r for r in self.data if hasattr(r, 'report_id') and r.report_id == report_id), None)
        if not report:
            return f"Отчет с ID {report_id} не найден в данных технолога."
        return f"Информация об отчете (ID {report_id}):\n{report}"

    def adjustEquipment(self, equipment: Equipment, adjustment: dict):
        if not isinstance(adjustment, dict):
            return "Настройки должны быть в формате словаря."

        for key, value in adjustment.items():
            try:
                equipment.update_setting(key, value)
            except ValueError as e:
                return f"Ошибка настройки: {e}"

        equipment.save()  # Сохраняем изменения в базе данных
        return f"Оборудование {equipment.name} успешно настроено с параметрами: {adjustment}."

    def getData(self):
        if not self.data:
            return "Нет доступных данных."
        return [f"Тип данных: {d.data_type}, Значение: {d.value}" for d in self.data]

    def viewReports(self):
        if not self.data:
            return "Нет отчетов для просмотра."

        report_list = [
            f"Тип данных: {d.data_type}, Значение: {d.value}"
            for d in self.data
            if hasattr(d, 'report_id')
        ]
        return "\n".join(report_list)
