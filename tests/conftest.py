import pytest
from app.interpolate import ProductSales
from datetime import datetime, date, timedelta


@pytest.fixture
def current() -> ProductSales:
    today = datetime.combine(date.today(), datetime.min.time())
    return ProductSales(delta=11, total=21, date=today, product_id=9)


@pytest.fixture
def prev_two_days() -> ProductSales:
    today = datetime.combine(date.today(), datetime.min.time())
    two_days_back = today - timedelta(days=2)
    return ProductSales(delta=5, total=10, date=two_days_back, product_id=9)


@pytest.fixture
def interpolated_result_two_days(prev_two_days) -> ProductSales:
    today = datetime.combine(date.today(), datetime.min.time())
    product_sale_1 = ProductSales(delta=6, total=21, date=today, product_id=9)
    product_sale_2 = ProductSales(
        delta=5, total=15, date=today - timedelta(days=1), product_id=9
    )
    return [product_sale_1, product_sale_2, prev_two_days]


@pytest.fixture
def prev() -> ProductSales:
    today = datetime.combine(date.today(), datetime.min.time())
    prev_date = today - timedelta(days=1)
    return ProductSales(delta=5, total=10, date=prev_date, product_id=9)


@pytest.fixture
def interpolated_result_one_day(current, prev) -> ProductSales:
    return [current, prev]
