from __future__ import annotations
from Date import Date

from Equipment import Equipment


class InventoryItem(Equipment):
    def __init__(self,
                username: str,
                user_id: int,
                name: str, 
                serial_number: int, 
                purchase_date: Date, 
                price: int) -> InventoryItem:
        self.__username = username
        self.__user_id = int(user_id)
        super().__init__(
            name=name,
            serial_number=serial_number,
            purchase_date=purchase_date,
            price=price
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, InventoryItem):
            return self.__dict__ == other.__dict__
        return False
    
    def __ne__(self, other: object):
        return not self.__eq__(other)

    def get_equipment(self) -> Equipment:
        return Equipment(
            name=self.get_name(),
            serial_number=self.get_serial_number(),
            purchase_date=self.get_purchase_date(),
            price=self.get_price()
        )

    def get_username(self) -> str:
        return self.__username
    
    def get_user_id(self) -> str:
        return self.__user_id
    
    def to_csv(self) -> str:
        return f"{self.__username} {self.__user_id} {super().to_csv()}"
    
    @staticmethod
    def from_csv(csv_string: str) -> str:
        parts = csv_string.split(" ")
        username = parts[0]
        user_id = parts[1]
        equipment_data = " ".join(parts[2:])
        equipment = Equipment.from_csv(equipment_data)

        return InventoryItem(
            username=username,
            user_id=user_id,
            name=equipment.get_name(),
            price=equipment.get_price(),
            purchase_date=equipment.get_purchase_date(),
            serial_number=equipment.get_serial_number()
        )
    
    def __str__(self):
        return self.to_csv()