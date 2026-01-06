from typing import Dict, Optional
from uuid import UUID
from domain.entities.order import Order
from application.interfaces.repository import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._orders: Dict[UUID, Order] = {}

    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        return self._orders.get(order_id)

    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order
