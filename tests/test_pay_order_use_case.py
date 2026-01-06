import pytest
from uuid import uuid4
from decimal import Decimal
from domain.entities.order import Order
from domain.entities.order_line import OrderLine
from domain.value_objects.money import Money
from infrastructure.repositories.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.payment.fake_payment_gateway import FakePaymentGateway
from application.use_cases.pay_order import PayOrderUseCase


class TestPayOrderUseCase:
    @pytest.fixture
    def setup(self):
        self.repository = InMemoryOrderRepository()
        self.payment_gateway = FakePaymentGateway()
        self.use_case = PayOrderUseCase(self.repository, self.payment_gateway)
        
        # Создаем тестовый заказ
        self.customer_id = uuid4()
        self.order = Order(customer_id=self.customer_id)
        
        line = OrderLine(
            product_id=uuid4(),
            product_name="Test Product",
            quantity=2,
            unit_price=Money(Decimal("25.00"))
        )
        self.order.add_order_line(line)
        
        self.repository.save(self.order)
        
        return self.order.order_id

    def test_successful_payment(self, setup):
        """Успешная оплата корректного заказа"""
        order_id = setup
        
        success, message = self.use_case.execute(order_id)
        
        assert success is True
        assert "paid successfully" in message
        
        # Проверяем, что заказ сохранен с правильным статусом
        saved_order = self.repository.get_by_id(order_id)
        assert saved_order.status.value == "paid"
        assert saved_order.paid_at is not None
        
        # Проверяем, что платежный шлюз был вызван
        assert len(self.payment_gateway.charges) == 1
        charge = self.payment_gateway.charges[0]
        assert charge['order_id'] == order_id
        assert charge['amount'] == Decimal("50.00")

    def test_payment_empty_order(self):
        """Ошибка при оплате пустого заказа"""
        # Создаем пустой заказ
        empty_order = Order(customer_id=uuid4())
        self.repository.save(empty_order)
        
        success, message = self.use_case.execute(empty_order.order_id)
        
        assert success is False
        assert "Cannot pay empty order" in message

    def test_double_payment_error(self, setup):
        """Ошибка при повторной оплате"""
        order_id = setup
        
        # Первая оплата - успешная
        success1, _ = self.use_case.execute(order_id)
        assert success1 is True
        
        # Вторая попытка оплаты
        success2, message2 = self.use_case.execute(order_id)
        
        assert success2 is False
        assert "Order already paid" in message2

    def test_order_not_found(self):
        """Ошибка при оплате несуществующего заказа"""
        non_existent_id = uuid4()
        
        success, message = self.use_case.execute(non_existent_id)
        
        assert success is False
        assert "not found" in message

    def test_payment_gateway_failure(self):
        """Ошибка при сбое платежного шлюза"""
        # Создаем use case с падающим платежным шлюзом
        failing_gateway = FakePaymentGateway(should_fail=True)
        use_case = PayOrderUseCase(self.repository, failing_gateway)
        
        # Создаем заказ
        order = Order(customer_id=uuid4())
        line = OrderLine(
            product_id=uuid4(),
            product_name="Product",
            quantity=1,
            unit_price=Money(Decimal("10.00"))
        )
        order.add_order_line(line)
        self.repository.save(order)
        
        success, message = use_case.execute(order.order_id)
        
        assert success is False
        assert "Payment gateway charge failed" in message
        
        # Заказ не должен быть помечен как оплаченный
        saved_order = self.repository.get_by_id(order.order_id)
        assert saved_order.status.value == "created"
