from app.models.user import User
from app.models.report import Report


class Manager(User):
    def __init__(self, user_id, name, email, department=None):
        super().__init__(user_id, name, email)
        self.department = department
        self.reports = []  # Менеджер может управлять списком отчетов, связанных с отделом

    def viewReports(self):
        if not self.reports:
            return f"В отделе {self.department} нет доступных отчетов."

        report_list = [f"ID: {r.report_id}, Title: {r.title}" for r in self.reports]
        return f"Отчеты отдела {self.department}:\n" + "\n".join(report_list)

    def getReportInfo(self, report_id):
        report = next((r for r in self.reports if r.report_id == report_id), None)
        if not report:
            return f"Отчет с ID {report_id} не найден в отделе {self.department}."

        return (
            f"Детали отчета (ID: {report_id}):\n"
            f"Title: {report.title}\nContent: {report.content}"
        )

    def setDepartment(self, department):
        self.department = department
        return f"Менеджер {self.username} теперь руководит отделом {department}."

    def getDepartment(self):
        return self.department

    def approveChanges(self, changes):
        # Пример логики: проверить содержание изменений
        if not changes:
            return f"Нет изменений для утверждения в отделе {self.department}."

        # Одобрить изменения
        approved_changes = []
        for change in changes:
            approved_changes.append(f"Изменение '{change}' одобрено.")

        return f"Все изменения для отдела {self.department} успешно утверждены:\n" + "\n".join(approved_changes)
