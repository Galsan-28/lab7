from uuid import UUID
from domain.value_objects.money import Money
from application.interfaces.payment_gateway import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    def __init__(self, should_fail: bool = False):
        self.should_fail = should_fail
        self.charges = []

    def charge(self, order_id: UUID, money: Money) -> bool:
        # Сохраняем историю платежей для тестирования
        self.charges.append({
            'order_id': order_id,
            'amount': money.amount,
            'currency': money.currency
        })
        
        if self.should_fail:
            return False
            
        return True
