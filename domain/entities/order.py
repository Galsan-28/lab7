from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from decimal import Decimal
from domain.value_objects.money import Money
from domain.entities.order_line import OrderLine


class OrderStatus(Enum):
    CREATED = "created"
    PAID = "paid"
    CANCELLED = "cancelled"


@dataclass
class Order:
    customer_id: UUID
    order_lines: List[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)
    paid_at: datetime = None
    order_id: UUID = None

    def __post_init__(self):
        if self.order_id is None:
            self.order_id = uuid4()
        self._validate_invariants()

    def _validate_invariants(self):
        """Проверка инвариантов агрегата"""
        if self.status == OrderStatus.PAID and not self.order_lines:
            raise ValueError("Cannot pay empty order")
        
        # Проверка суммы
        calculated_total = sum((line.total.amount for line in self.order_lines), 
                              Decimal("0"))
        if hasattr(self, '_total') and self._total.amount != calculated_total:
            raise ValueError("Total amount does not match order lines sum")

    def add_order_line(self, order_line: OrderLine):
        """Добавить строку заказа"""
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify order after payment")
        self.order_lines.append(order_line)
        self._validate_invariants()

    def remove_order_line(self, line_id: UUID):
        """Удалить строку заказа"""
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify order after payment")
        self.order_lines = [line for line in self.order_lines 
                           if line.line_id != line_id]
        self._validate_invariants()

    def pay(self):
        """Оплатить заказ"""
        if self.status == OrderStatus.PAID:
            raise ValueError("Order already paid")
        
        if not self.order_lines:
            raise ValueError("Cannot pay empty order")
        
        self.status = OrderStatus.PAID
        self.paid_at = datetime.now()
        self._validate_invariants()

    @property
    def total(self) -> Money:
        """Общая сумма заказа"""
        if not self.order_lines:
            return Money(Decimal("0"))
        
        total_amount = sum((line.total.amount for line in self.order_lines), 
                          Decimal("0"))
        return Money(total_amount, self.order_lines[0].unit_price.currency)

    def is_empty(self) -> bool:
        """Проверка, пустой ли заказ"""
        return len(self.order_lines) == 0
