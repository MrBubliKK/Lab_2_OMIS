import sqlite3
from config.settings import DATABASE_PATH  # Убедитесь, что путь к базе данных указан правильно

class Equipment:
    def __init__(self, name, weight, size, temperature, condition, id=None):
        self.id = id
        self.name = name
        self.settings = {
            "weight": int(weight),
            "size": int(size),
            "temperature": int(temperature)
        }
        self.condition = bool(condition)

    def setNewSettings(self, weight, size, temperature):
        """Установить новые значения для параметров веса, размера и температуры."""
        self.settings["weight"] = int(weight)
        self.settings["size"] = int(size)
        self.settings["temperature"] = int(temperature)
        print("Настройки обновлены успешно.")

    def getSettings(self):
        """Вернуть текущие настройки оборудования."""
        return self.settings

    def getCondition(self):
        """Вернуть текущее состояние оборудования."""
        return "Рабочее" if self.condition else "Не рабочее"

    def update_setting(self, setting_name, value):
        """Обновить одно из значений настройки, если оно существует."""
        if setting_name in self.settings:
            self.settings[setting_name] = int(value)
        else:
            raise ValueError(f"Setting '{setting_name}' does not exist in equipment settings.")

    def toggle_condition(self):
        """Переключить состояние condition между True и False."""
        self.condition = not self.condition

    def display_info(self):
        """Вывести информацию об оборудовании."""
        print(f"Название оборудования: {self.name}")
        print("Настройки:")
        for setting, value in self.settings.items():
            print(f"  {setting.capitalize()}: {value}")
        print(f"Состояние: {self.getCondition()}")

    def save(self):
        """Сохранить оборудование в базу данных или обновить его, если уже существует."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        if self.id is None:  # Если оборудование еще не существует в БД
            cursor.execute("""
                INSERT INTO equipment (name, weight, size, temperature, condition)
                VALUES (?, ?, ?, ?, ?)
            """, (self.name, self.settings["weight"], self.settings["size"], self.settings["temperature"], int(self.condition)))
            self.id = cursor.lastrowid  # Устанавливаем ID для нового оборудования
        else:  # Обновление существующей записи
            cursor.execute("""
                UPDATE equipment
                SET name = ?, weight = ?, size = ?, temperature = ?, condition = ?
                WHERE id = ?
            """, (self.name, self.settings["weight"], self.settings["size"], self.settings["temperature"], int(self.condition), self.id))

        conn.commit()
        conn.close()
        print("Оборудование сохранено в базу данных.")

    @classmethod
    def load(cls, equipment_id):
        """Загрузить оборудование из базы данных по ID."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, weight, size, temperature, condition
            FROM equipment
            WHERE id = ?
        """, (equipment_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            id, name, weight, size, temperature, condition = result
            return cls(name, weight, size, temperature, bool(condition), id=id)
        else:
            print(f"Оборудование с ID {equipment_id} не найдено.")
            return None

    @classmethod
    def load_all(cls):
        """Загрузить все оборудование из базы данных."""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, weight, size, temperature, condition
            FROM equipment
        """)
        results = cursor.fetchall()
        conn.close()

        equipment_list = []
        for result in results:
            id, name, weight, size, temperature, condition = result
            equipment = cls(name, weight, size, temperature, bool(condition), id=id)
            equipment_list.append(equipment)

        return equipment_list

    @staticmethod
    def get_by_id(equipment_id):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, weight, size, temperature, condition FROM equipment WHERE id=?", (equipment_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Equipment(id=row[0], name=row[1], weight=row[2], size=row[3], temperature=row[4], condition=row[5])
        return None


    def set_condition(self, condition):
        """Устанавливает новое состояние оборудования (рабочее или нерабочее)."""
        self.condition = bool(condition)
