import pytest
from uuid import uuid4, UUID
from decimal import Decimal
from datetime import datetime
from domain.entities.order import Order, OrderStatus
from domain.entities.order_line import OrderLine
from domain.value_objects.money import Money


class TestOrderDomain:
    def test_create_order_with_lines(self):
        """Тест создания заказа со строками"""
        customer_id = uuid4()
        order = Order(customer_id=customer_id)
        
        line1 = OrderLine(
            product_id=uuid4(),
            product_name="Product 1",
            quantity=2,
            unit_price=Money(Decimal("10.50"))
        )
        
        line2 = OrderLine(
            product_id=uuid4(),
            product_name="Product 2",
            quantity=1,
            unit_price=Money(Decimal("20.00"))
        )
        
        order.add_order_line(line1)
        order.add_order_line(line2)
        
        assert order.total.amount == Decimal("41.00")
        assert len(order.order_lines) == 2
        assert order.status == OrderStatus.CREATED

    def test_cannot_pay_empty_order(self):
        """Нельзя оплатить пустой заказ"""
        order = Order(customer_id=uuid4())
        
        with pytest.raises(ValueError, match="Cannot pay empty order"):
            order.pay()

    def test_cannot_pay_already_paid_order(self):
        """Нельзя оплатить уже оплаченный заказ"""
        order = Order(customer_id=uuid4())
        line = OrderLine(
            product_id=uuid4(),
            product_name="Product",
            quantity=1,
            unit_price=Money(Decimal("10.00"))
        )
        order.add_order_line(line)
        
        order.pay()
        
        with pytest.raises(ValueError, match="Order already paid"):
            order.pay()

    def test_cannot_modify_order_after_payment(self):
        """Нельзя изменить заказ после оплаты"""
        order = Order(customer_id=uuid4())
        line = OrderLine(
            product_id=uuid4(),
            product_name="Product",
            quantity=1,
            unit_price=Money(Decimal("10.00"))
        )
        order.add_order_line(line)
        order.pay()
        
        new_line = OrderLine(
            product_id=uuid4(),
            product_name="New Product",
            quantity=1,
            unit_price=Money(Decimal("20.00"))
        )
        
        with pytest.raises(ValueError, match="Cannot modify order after payment"):
            order.add_order_line(new_line)

    def test_total_calculation(self):
        """Правильный расчет общей суммы"""
        order = Order(customer_id=uuid4())
        
        line1 = OrderLine(
            product_id=uuid4(),
            product_name="Product 1",
            quantity=3,
            unit_price=Money(Decimal("5.00"))
        )
        
        line2 = OrderLine(
            product_id=uuid4(),
            product_name="Product 2",
            quantity=2,
            unit_price=Money(Decimal("7.50"))
        )
        
        order.add_order_line(line1)
        order.add_order_line(line2)
        
        assert order.total.amount == Decimal("30.00")  # 3*5 + 2*7.5 = 30
