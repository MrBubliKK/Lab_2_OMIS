from app.models.equipment import Equipment


class EquipmentController:

    def add_equipment(self, name, weight, size, temperature, condition):
        equipment = Equipment(
            name=name,
            weight=weight,
            size=size,
            temperature=temperature,
            condition=condition
        )
        equipment.save()

    def update_settings(self, equipment_id, weight, size, temperature):
        equipment = Equipment.load(equipment_id)
        if equipment:
            equipment.setNewSettings(weight, size, temperature)
            equipment.save()


    def view_equipment(self, equipment_id):
        equipment = Equipment.load(equipment_id)
        if equipment:
            settings = equipment.getSettings()
            condition = equipment.getCondition()

    def view_all_equipment(self):
        """Теперь метод возвращает список оборудования."""
        equipment_list = Equipment.load_all()
        if not equipment_list:
            print("Нет оборудования для отображения.")
        return equipment_list  # Теперь возвращаем список оборудования
