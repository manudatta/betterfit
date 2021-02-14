import requests
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from datetime import datetime, timedelta

# pretend this url accept post requests with a single json CupSale object as the payload
# real requests here will fail
api_url = "https://api.rainforest.com/sales"


@dataclass_json
@dataclass
class ProductSales:
    # change in total number of cups sold
    delta: int = None
    # totol number of cups sold
    total: int = None
    date: datetime = None
    product_id: int = None


def allocate(bin_count: int, item_count: int) -> list[int]:
    """
    Allocates item_count into groups of bin_count
    If we cannot divide evenly we find mininum which should be allocated
    to each bin and rest we distribute evenly starting from first bin till
    all items are accounted for
    """
    assert bin_count > 0, item_count >= 0
    per_bin, left_over = divmod(item_count, bin_count)
    allocations = []
    for _ in range(bin_count):
        this_allocation = per_bin
        if left_over > 0:
            this_allocation += 1
            left_over -= 1
        allocations.append(this_allocation)
    return allocations


def get_missing_days(start: datetime, end: datetime) -> list[datetime]:
    """
    return a list of days between start and end excluding current and prev
    """
    assert start > end
    one_day = timedelta(days=-1)
    missing_days, current = [], start + one_day
    while current > end:
        print(current)
        missing_days.append(current)
        current += one_day
    return missing_days


def get_interpolated_list(
    current: ProductSales, prev: ProductSales
) -> list[ProductSales]:
    product_id = current.product_id
    current_date = current.date
    prev_date = prev.date
    missing_days = get_missing_days(current_date, prev_date)
    allocations = allocate(len(missing_days) + 1, current.delta)
    total = prev.total
    product_sales_interpolated = [prev]
    for i, delta in enumerate(allocations[::-1]):
        date = prev_date + timedelta(days=i + 1)
        total += delta
        product_sale = ProductSales(
            delta=delta, total=total, date=date, product_id=product_id
        )
        product_sales_interpolated.insert(0, product_sale)
    return product_sales_interpolated


def interpolate_and_post(current: ProductSales, prev: ProductSales) -> None:
    """
    Recieves the current ProductSales and last ProductSales we have in our database and posts new
    cup sales objects to our api.

    If there are missing days between current and prev, then we must do the following things:
    1. Create a ProductSales object for each missing day
    2. Split the current day's delta evenly between current day and all missing days.
       These values for delta should be integers and it is okay if some values are 1 above/below the others.
       The important thing is that the sum of delta values still adds up to the current CupSale object's original delta
    3. Set the total, date, and product_id fields to the correct values

    Then, post the current day's cup sales to

    For example (note that the date field should be a datetime object, not a string):
    current = ProductSales(delta=11, total=21, date=today, product_id=9)
    prev = ProductSales(delta=5, total=10, date=2 days ago, product_id=9)

    These should be posted
    ProductSales(delta=6, total=21, date=today, product_id=9)
    ProductSales(delta=5, total=15, date=1 day ago, product_id=9)
    6 + 5 adds up to 11, could have been in a different order so long as the totals for each day are correct
    """
    assert current.date > prev.date
    results = get_interpolated_list(current, prev)
    json_payload = [obj.to_json() for obj in results]
    return requests.post(api_url, json=json_payload)
