from app import create_app, db

# Создаём приложение
app = create_app()

# Запуск приложения
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц в базе данных
    app.run(debug=True)
