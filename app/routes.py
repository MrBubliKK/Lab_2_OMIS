import os

from flask import render_template, request, redirect, url_for, flash, session, Blueprint, current_app
from werkzeug.utils import secure_filename

from app.controllers.auth_controller import AuthController
from app.models.check import Check
from app.models.equipment import Equipment
from app.models.report import Report
from app.models.settings import Settings
from app.models.test import Test
from app.controllers.profile_controller import ProfileController
from app.controllers.report_controller import ReportController
from app.controllers.check_controller import CheckController
from app.models.user import User

routes = Blueprint('routes', __name__)

# Инициализация контроллеров
auth_controller = AuthController()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Роуты для входа и регистрации
@routes.route('/')
def index():
    return render_template('index.html')


@routes.route('/authenticate', methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        user = auth_controller.login(login, password)
        if user:
            return redirect(url_for('routes.main_menu', user_id=user.id))
        else:
            flash("Неверные логин или пароль.")
    return render_template('authenticate.html')


@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        role = request.form.get('role')
        login = request.form.get('login')
        password = request.form.get('password')
        birthdate = request.form.get('birthdate')

        # Получение аватара из запроса
        avatar_file = request.files.get('avatar')

        # Регистрация пользователя
        auth_controller.register(
            username=username,
            role=role,
            login=login,
            password=password,
            birthdate=birthdate,
            avatar_file=avatar_file  # Передаем сам файл аватара, а не его имя
        )

        flash("Регистрация успешна. Пожалуйста, войдите.")
        return redirect(url_for('routes.authenticate'))

    return render_template('register.html')


@routes.route('/main_menu/<user_id>', methods=['GET', 'POST'])
def main_menu(user_id):
    # Получение информации о пользователе из базы данных
    user = auth_controller.get_user_by_id(user_id)
    if not user:
        flash("Пользователь не найден.")
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        choice = request.form.get('choice')

        # Обработка действий пользователя в зависимости от его роли
        if choice == "1":  # Профиль
            return redirect(url_for('routes.profile', user_id=user.id))
        elif choice == "2":  # Отчёты
            return redirect(url_for('routes.reports', user_id=user.id))
        elif choice == "3" and user.role in ['operator', 'engineer']:  # Проверка
            return redirect(url_for('routes.check_menu', user_id=user.id))
        elif choice == "4" and user.role == 'engineer':  # Анализ данных
            return redirect(url_for('routes.data_analysis', user_id=user.id))
        elif choice == "5" and user.role == 'technologist':  # Оборудование
            return redirect(url_for('routes.equipment_list', user_id=user.id))
        elif choice == "6":
            return redirect(url_for('routes.index'))
        else:
            flash("Некорректный выбор или у вас недостаточно прав для выполнения этого действия.")

    # Рендерим главное меню с учетом роли пользователя
    return render_template('main_menu.html', user=user)


def allowed_file(filename):
    """Проверяем, разрешен ли формат файла."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@routes.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    # Проверка авторизации пользователя
    if 'user_id' not in session or session['user_id'] != int(user_id):
        flash("Пожалуйста, войдите, чтобы получить доступ к профилю.")
        return redirect(url_for('routes.authenticate'))

    # Получение пользователя
    user = User.get_by_id(user_id)
    profile_controller = ProfileController(user)

    if request.method == 'POST':
        # Обработка данных профиля
        updated_data = {
            'username': request.form.get('username', user.username),
            'role': request.form.get('role', user.role),
            'login': request.form.get('login', user.login),
            'password': request.form.get('password', user.password),
            'birthdate': request.form.get('birthdate', user.birthdate)
        }

        # Обработка загрузки аватара
        if 'avatar' in request.files and request.files['avatar']:
            file = request.files['avatar']
            if file and allowed_file(file.filename):
                # Передаем сам файл в метод, а не его имя
                updated_data['avatar'] = file

        # Обновляем другие данные
        profile_controller.update_profile(updated_data, avatar=updated_data.get('avatar'))
        flash("Профиль обновлен!")
        return redirect(url_for('routes.profile', user_id=user.id))

    return render_template('profile.html', user=user)



@routes.route('/reports/<user_id>', methods=['GET', 'POST'])
def reports(user_id):
    # Проверка авторизации
    if 'user_id' not in session or session['user_id'] != int(user_id):
        flash("Пожалуйста, войдите, чтобы получить доступ к отчетам.")
        return redirect(url_for('routes.login'))

    # Получаем пользователя и контроллер отчетов
    user = User.get_by_id(user_id)
    report_controller = ReportController(user.id)

    if request.method == 'POST':
        report_action = request.form.get('report_action')

        if report_action == '1':
            return report_controller.show_all_reports()

        elif report_action == '2':
            # Создание нового отчета
            name = request.form.get('name')
            info = request.form.get('info')
            if name and info:
                report_controller.create_new_report({'name': name, 'info': info})
                flash("Новый отчет успешно создан!")
                return redirect(url_for('routes.reports', user_id=user.id))
            else:
                flash("Название и описание отчета обязательны.")

    # Отображение всех отчетов
    reports = report_controller.show_all_reports()
    return render_template('reports.html', user=user, reports=reports)


@routes.route('/reports/<user_id>/<report_id>', methods=['GET'])
def show_report_details(user_id, report_id):
    report = Report.get_by_id(report_id)
    if report:
        report_controller = ReportController(report.user_id)
        # report_controller.view.show_report_details(report)
        return render_template('report_details.html', report=report)
    else:
        flash("Отчет не найден.")
        return redirect(url_for('routes.reports', user_id=user_id))


@routes.route('/check_menu/<user_id>', methods=['GET', 'POST'])
def check_menu(user_id):
    # Проверяем авторизацию пользователя
    if 'user_id' not in session or session['user_id'] != int(user_id):
        flash("Пожалуйста, войдите, чтобы получить доступ к проверкам.")
        return redirect(url_for('routes.authenticate'))

    # Получаем все тесты и оборудование
    all_tests = Test.load_all()
    all_equipment = Equipment.load_all()
    results = []

    # Инициализация контроллера проверки
    check_controller = CheckController(user_id=user_id)

    if request.method == 'POST':
        # Создание нового теста
        if 'create_test' in request.form:
            test_name = request.form.get('test_name')
            weight = request.form.get('weight')
            size = request.form.get('size')
            temperature = request.form.get('temperature')
            if test_name and weight and size and temperature:
                new_test = Test(name=test_name, weight=int(weight), size=int(size), temperature=int(temperature))
                new_test.save()
                flash("Новый тест успешно создан!")
                return redirect(url_for('routes.check_menu', user_id=user_id))
            else:
                flash("Все поля обязательны для заполнения.")

        # Запуск проверки
        elif 'run_check' in request.form:
            check_name = request.form.get('check_name')
            selected_equipment_id = request.form.get('equipment_id')  # Получаем ID оборудования
            selected_test_ids = request.form.getlist('test_ids')  # Получаем список ID тестов

            print(check_name)
            print(selected_equipment_id)
            print(selected_test_ids)

            if check_name and selected_equipment_id and selected_test_ids:
                # Загружаем оборудование
                equipment = Equipment.get_by_id(int(selected_equipment_id))
                selected_tests = [Test.get_by_id(int(test_id)) for test_id in selected_test_ids]

                if not equipment:
                    flash("Некорректное оборудование.")
                    return redirect(url_for('routes.check_menu', user_id=user_id))

                if not selected_tests:
                    flash("Выбранные тесты недействительны.")
                    return redirect(url_for('routes.check_menu', user_id=user_id))

                # Создаем настройки для проверки
                settings = Settings(count=len(selected_tests), fallability=0.0, tests=selected_tests)

                # Создаем объект проверки
                check = Check(name=check_name, settings=settings)
                try:
                    average_percentage = check.calculate_average_percentage(
                        equipment=equipment,
                        tests=selected_tests
                    )
                except ValueError as e:
                    flash(str(e))
                    return redirect(url_for('routes.check_menu', user_id=user_id))

                # Округляем процент
                average_percentage = round(average_percentage, 1)

                # Обновляем настройки с расчетом fallability
                settings.fallability = average_percentage / 100

                # Сохраняем проверку
                check.save(selected_equipment_id)

                # Отображаем результат
                flash(f"Проверка '{check_name}' выполнена. Средний результат: {average_percentage:.1f}%.")
                results.append({
                    "check_name": check_name,
                    "average_percentage": average_percentage,
                })

                return render_template(
                    'check_menu.html',
                    user_id=user_id,
                    tests=all_tests,
                    equipment=all_equipment,
                    results=results
                )

            else:
                flash("Пожалуйста, заполните все поля для запуска проверки.")
                return redirect(url_for('routes.check_menu', user_id=user_id))

    # Возвращаем представление для GET-запроса и пустого POST
    return render_template(
        'check_menu.html',
        user_id=user_id,
        tests=all_tests,
        equipment=all_equipment,
        results=results
    )



@routes.route('/data_analysis/<user_id>', methods=['GET', 'POST'])
def data_analysis(user_id):
    show_date = False
    show_count = False
    show_fallability = False

    if request.method == 'POST':
        # Получаем значения галочек из формы
        show_date = 'show_date' in request.form
        show_count = 'show_count' in request.form
        show_fallability = 'show_fallability' in request.form

        # Обновляем отображение для всех проверок в базе данных
        Check.update_display_for_all('date', show_date)
        Check.update_display_for_all('count', show_count)
        Check.update_display_for_all('fallability', show_fallability)

    # Загружаем все проверки с обновленными флагами отображения
    checks = Check.load_all()

    # Передаем флаги и список проверок в шаблон
    return render_template('data_analysis.html', checks=checks, show_date=show_date, show_count=show_count,
                           show_fallability=show_fallability, user_id=user_id)


@routes.route('/equipment_list/<int:user_id>', methods=['GET', 'POST'])
def equipment_list(user_id):
    # Загружаем все оборудование
    equipment = Equipment.load_all()  # Замените это на правильный метод для получения списка оборудования

    if request.method == 'POST':
        selected_equipment_id = request.form.get('equipment_id')  # Получаем ID выбранного оборудования
        equipment = Equipment.get_by_id(selected_equipment_id)  # Получаем данные об оборудовании

        return redirect(url_for('routes.edit_equipment', equipment_id=selected_equipment_id, user_id=user_id))

    return render_template('equipment_list.html', equipment=equipment, user_id=user_id)


@routes.route('/edit_equipment/<int:equipment_id>/<int:user_id>', methods=['GET', 'POST'])
def edit_equipment(equipment_id, user_id):
    equipment = Equipment.get_by_id(equipment_id)  # Получаем информацию о выбранном оборудовании

    if request.method == 'POST':
        # Обрабатываем изменения настроек
        equipment.name = request.form['name']
        equipment.setNewSettings(
            request.form['weight'],
            request.form['size'],
            request.form['temperature']
        )

        # Преобразуем строковое значение в булево для состояния
        condition = request.form.get('condition') == "True"  # Преобразуем "True" в True, "False" в False
        equipment.condition = condition

        equipment.save()  # Сохраняем изменения в базе данных

        # Перенаправляем обратно в список оборудования
        return redirect(url_for('routes.equipment_list', user_id=user_id))

    return render_template('edit_equipment.html', equipment=equipment, user_id=user_id)


@routes.route('/exit', methods=['GET'])
def exit_app():
    """Маршрут для завершения работы приложения."""
    os._exit(0)  # Завершить выполнение программы
