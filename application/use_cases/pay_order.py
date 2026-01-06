from typing import Tuple
from uuid import UUID
from application.interfaces.repository import OrderRepository
from application.interfaces.payment_gateway import PaymentGateway
from domain.entities.order import Order
from domain.value_objects.money import Money


class PayOrderUseCase:
    def __init__(
        self,
        order_repository: OrderRepository,
        payment_gateway: PaymentGateway
    ):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway

    def execute(self, order_id: UUID) -> Tuple[bool, str]:
        """
        Выполнить оплату заказа
        
        Returns:
            Tuple[bool, str]: (успех, сообщение)
        """
        # 1. Загружаем заказ
        order = self.order_repository.get_by_id(order_id)
        if not order:
            return False, f"Order {order_id} not found"

        try:
            # 2. Выполняем доменную операцию оплаты
            order.pay()
            
            # 3. Вызываем платежный шлюз
            payment_success = self.payment_gateway.charge(order_id, order.total)
            
            if not payment_success:
                # В реальном приложении здесь нужна компенсирующая транзакция
                return False, "Payment gateway charge failed"
            
            # 4. Сохраняем обновленный заказ
            self.order_repository.save(order)
            
            return True, f"Order {order_id} paid successfully"
            
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Unexpected error: {str(e)}"
