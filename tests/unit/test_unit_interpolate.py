from datetime import datetime
from app.interpolate_and_post import (
    get_missing_days,
    allocate,
    get_interpolated_list,
    ProductSales,
)


def test_get_missing_days():
    current = datetime(2020, 2, 12)
    prev = datetime(2020, 2, 10)
    missing_days = [datetime(2020, 2, 11)]
    assert get_missing_days(current, prev) == missing_days, "wrong list of missing days"
    # test when function should return empty list
    current = datetime(2020, 2, 12)
    prev = datetime(2020, 2, 11)
    missing_days = []
    assert get_missing_days(current, prev) == missing_days, "missing days is not empty"


def test_allocate():
    bin_count = 1
    item_count = 5
    assert [5] == allocate(
        bin_count, item_count
    ), "wrong allocation for single bin count"

    bin_count = 2
    item_count = 11
    assert [6, 5] == allocate(
        bin_count, item_count
    ), "wrong allocation for two bin count with non even items"

    bin_count = 3
    item_count = 9
    assert [3, 3, 3] == allocate(
        bin_count, item_count
    ), "wrong allocation for three bin count with even items"


def test_interpolate_case_missing_days(
    current: ProductSales,
    prev_two_days: ProductSales,
    interpolated_result_two_days: list[ProductSales],
):
    results = get_interpolated_list(current, prev_two_days)
    assert interpolated_result_two_days == results


def test_interpolate(
    current: ProductSales,
    prev: ProductSales,
    interpolated_result_one_day: list[ProductSales],
):
    results = get_interpolated_list(current, prev)
    assert interpolated_result_one_day == results
