import pytest
from decimal import Decimal
from domain.value_objects.money import Money


class TestMoneyValueObject:
    def test_money_creation(self):
        """Создание объекта Money"""
        money = Money(Decimal("100.50"))
        assert money.amount == Decimal("100.50")
        assert money.currency == "USD"

    def test_money_addition(self):
        """Сложение Money"""
        money1 = Money(Decimal("50.00"))
        money2 = Money(Decimal("25.50"))
        
        result = money1 + money2
        assert result.amount == Decimal("75.50")

    def test_cannot_add_different_currencies(self):
        """Нельзя складывать деньги разных валют"""
        money1 = Money(Decimal("100.00"), "USD")
        money2 = Money(Decimal("100.00"), "EUR")
        
        with pytest.raises(ValueError, match="Cannot add money with different currencies"):
            money1 + money2

    def test_cannot_create_negative_money(self):
        """Нельзя создать отрицательную сумму"""
        with pytest.raises(ValueError, match="Money amount cannot be negative"):
            Money(Decimal("-10.00"))
