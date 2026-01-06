# lab7
## Лабораторная работа 7: Архитектура, слои и DDD-lite

## Описание
Реализация системы оплаты заказа с использованием слоистой архитектуры и DDD-lite.

## Структура проекта 
lab7/
├── domain/
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── order.py
│   │   └── order_line.py
│   └── value_objects/
│       ├── __init__.py
│       └── money.py
├── application/
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── repository.py
│   │   └── payment_gateway.py
│   └── use_cases/
│       ├── __init__.py
│       └── pay_order.py
├── infrastructure/
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── in_memory_order_repository.py
│   └── payment/
│       ├── __init__.py
│       └── fake_payment_gateway.py
├── tests/
│   ├── __init__.py
│   ├── test_money.py
│   ├── test_order.py
│   └── test_pay_order_use_case.py
├── requirements.txt
└── README.md
