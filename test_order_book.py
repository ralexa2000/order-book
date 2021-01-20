import pytest
import random

from order_book import OrderBook


def test_place_first_order():
    """
    Place a first order into order book
    """
    ob = OrderBook()
    ob.place_order('1', 10, 2, 'ask')
    assert ob.orders == [{
        'order_id': '1',
        'price': 10,
        'quantity': 2,
        'order_type': 'ask'
    }]
    assert ob.prices == [10]


def test_place_order_in_the_middle():
    """
    Place an order in the middle of a full order book
    """
    ob = OrderBook()

    # first, place 10 orders with increasing prices
    expected_orders = []
    for i in range(1, 11):
        order = {
            'order_id': str(i),
            'price': i,
            'quantity': random.randint(1, 100),
            'order_type': random.choice(['bid', 'ask'])
        }
        expected_orders.append(order)
        ob.place_order(**order)
        assert ob.orders == expected_orders
        assert ob.prices == [o['price'] for o in expected_orders]

    # place one order in the middle of the order_book
    order = {
        'order_id': '11',
        'price': 6.5,
        'quantity': random.randint(1, 100),
        'order_type': random.choice(['bid', 'ask'])
    }
    ob.place_order(**order)
    expected_orders.insert(6, order)
    assert ob.orders == expected_orders
    assert ob.prices == [o['price'] for o in expected_orders]


def test_place_duplicate_order_id():
    """
    Place an order with an id that already exists in the order book
    """
    ob = OrderBook()
    ob.place_order('1', 10, 2, 'ask')
    with pytest.raises(ValueError):
        ob.place_order('1', 11, 3, 'bid')


def test_place_unknown_order_type():
    """
    Place an order with an unknown order type
    """
    ob = OrderBook()
    with pytest.raises(ValueError):
        ob.place_order('1', 1, 1, 'bed')


def test_cancel_order():
    """
    Check that order cancels correctly
    """
    ob = OrderBook()

    # first, place 10 orders with increasing prices
    expected_orders = []
    for i in range(1, 11):
        order = {
            'order_id': str(i),
            'price': i,
            'quantity': random.randint(1, 100),
            'order_type': random.choice(['bid', 'ask'])
        }
        expected_orders.append(order)
        ob.place_order(**order)

    # cancel order
    ob.cancel_order('6')
    del expected_orders[5]
    assert ob.orders == expected_orders
    assert ob.prices == [o['price'] for o in expected_orders]


def test_cancel_non_existing_order():
    """
    Check that method raises ValueError if order_id does not exist
    (when there are no other orders, and when there are other orders with
    different order_ids)
    """
    ob = OrderBook()
    with pytest.raises(ValueError):
        ob.cancel_order('1')
    ob.place_order('1', 10, 2, 'ask')
    with pytest.raises(ValueError):
        ob.cancel_order('2')


def test_get_order_info():
    """
    Check that method returns correct info about an order
    """
    ob = OrderBook()
    order = {
        'order_id': '10',
        'price': random.randint(1, 10),
        'quantity': random.randint(1, 100),
        'order_type': random.choice(['bid', 'ask'])
    }
    ob.place_order(**order)
    assert ob.get_order_info('10') == order


def test_get_info_non_existing_order():
    """
    Check that method raises ValueError if order_id does not exist
    (when there are no other orders, and when there are other orders with
    different order_ids)
    """
    ob = OrderBook()
    with pytest.raises(ValueError):
        ob.get_order_info('1')
    ob.place_order('1', 10, 2, 'ask')
    with pytest.raises(ValueError):
        ob.get_order_info('2')
