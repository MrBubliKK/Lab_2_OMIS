from flask import render_template, redirect, url_for, flash
from app.models.report import Report
from app.models.user import User

class ReportController:
    def __init__(self, user_id):
        self.user_id = user_id

    def show_all_reports(self):
        """Получает список всех отчетов пользователя."""
        reports = Report.get_all_reports()
        return reports

    def create_new_report(self, report_data):
        """Создает новый отчет с предоставленными данными."""
        new_report = Report(name=report_data['name'], info=report_data['info'], user_id=self.user_id)
        new_report.save_to_db()


