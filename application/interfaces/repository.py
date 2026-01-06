from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID
from domain.entities.order import Order


class OrderRepository(ABC):
    @abstractmethod
    def get_by_id(self, order_id: UUID) -> Optional[Order]:
        pass

    @abstractmethod
    def save(self, order: Order) -> None:
        pass
