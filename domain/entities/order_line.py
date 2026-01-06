from dataclasses import dataclass
from uuid import UUID, uuid4
from decimal import Decimal
from domain.value_objects.money import Money


@dataclass
class OrderLine:
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Money
    line_id: UUID = None

    def __post_init__(self):
        if self.line_id is None:
            self.line_id = uuid4()
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.unit_price.amount <= Decimal("0"):
            raise ValueError("Unit price must be positive")

    @property
    def total(self) -> Money:
        return Money(self.unit_price.amount * Decimal(self.quantity))
