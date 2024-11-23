import sqlite3

class Test:
    def __init__(self, name, weight, size, temperature, id=None):
        self.id = id
        self.name = name
        self.weight = weight
        self.size = size
        self.temperature = temperature

    def save(self):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute("""
                INSERT INTO tests (name, weight, size, temperature)
                VALUES (?, ?, ?, ?)
            """, (self.name, self.weight, self.size, self.temperature))
        else:
            cursor.execute("""
                UPDATE tests SET name=?, weight=?, size=?, temperature=? WHERE id=?
            """, (self.name, self.weight, self.size, self.temperature, self.id))
        conn.commit()
        conn.close()

    @staticmethod
    def load_all():
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, weight, size, temperature FROM tests")
        rows = cursor.fetchall()
        conn.close()
        return [Test(id=row[0], name=row[1], weight=row[2], size=row[3], temperature=row[4]) for row in rows]

    @staticmethod
    def get_by_id(test_id):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, weight, size, temperature FROM tests WHERE id=?", (test_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return Test(id=row[0], name=row[1], weight=row[2], size=row[3], temperature=row[4])
        return None

    def calculate_percentages(self, equipment):
        """
        Вычисляет процентное соотношение вес/размер/температура теста к оборудованию.
        Значения ограничиваются до 100%.
        """
        weight_percentage = min((equipment.settings["weight"] / self.weight) * 100, 100) if self.weight else 0
        size_percentage = min((equipment.settings["size"] / self.size) * 100, 100) if self.size else 0
        temperature_percentage = min((equipment.settings["temperature"] / self.temperature) * 100, 100) if self.temperature else 0

        result_precentage = (weight_percentage + size_percentage + temperature_percentage) / 3

        return {
            "result_precentage": result_precentage
        }
