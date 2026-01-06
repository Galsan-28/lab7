from abc import ABC, abstractmethod
from uuid import UUID
from domain.value_objects.money import Money


class PaymentGateway(ABC):
    @abstractmethod
    def charge(self, order_id: UUID, money: Money) -> bool:
        pass
