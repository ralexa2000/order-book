import random
import pytest

from order_book import OrderBook


@pytest.mark.parametrize('order_type', ['ask', 'bid'])
def test_place_first_order(order_type):
    """
    Place a first order into order book
    """
    ob = OrderBook()
    order = {
        'order_id': '1',
        'price': 10.5,
        'quantity': 2
    }
    ob.place_order(**order, order_type=order_type)
    if order_type == 'ask':
        assert ob.asks == [order]
        assert ob.bids == []
    else:
        assert ob.asks == []
        assert ob.bids == [order]


def test_place_order_in_the_middle():
    """
    Place an order in the middle of a full order book
    """
    ob = OrderBook()

    # firstly, place 5 asks and 5 bids with increasing prices
    expected_orders = {'ask': [], 'bid': []}
    for i in range(1, 6):
        for order_type in ('ask', 'bid'):
            order = {
                'order_id': f'{order_type} {i}',
                'price': i,
                'quantity': random.randint(1, 100)
            }
            ob.place_order(**order, order_type=order_type)
            expected_orders[order_type].append(order)

    # place 1 ask and 1 bid in the middle of orders list
    for order_type in ('ask', 'bid'):
        order = {
            'order_id': f'{order_type} 6',
            'price': 3.5,
            'quantity': random.randint(1, 100)
        }
        ob.place_order(**order, order_type=order_type)
        expected_orders[order_type].insert(3, order)
    assert ob.asks == expected_orders['ask']
    assert ob.bids == expected_orders['bid']


@pytest.mark.parametrize('order_type', ['ask', 'bid'])
def test_place_duplicate_order_id(order_type):
    """
    Place an order with an id that already exists in the order book
    """
    ob = OrderBook()
    ob.place_order('1', 10, 2, order_type)
    with pytest.raises(ValueError):
        ob.place_order('1', 11, 3, order_type)


def test_place_unknown_order_type():
    """
    Place an order with an unknown order type
    """
    ob = OrderBook()
    with pytest.raises(ValueError):
        ob.place_order('1', 1, 1, 'bed')


@pytest.mark.parametrize('order_type', ['ask', 'bid'])
def test_place_order_wrong_price_type(order_type):
    """
    Check that price could not be negative or zero
    """
    ob = OrderBook()
    with pytest.raises(ValueError):
        ob.place_order('1', -2, 2, order_type)
    with pytest.raises(ValueError):
        ob.place_order('1', 0, 2, order_type)


@pytest.mark.parametrize('order_type', ['ask', 'bid'])
def test_place_order_wrong_quantity_type(order_type):
    """
    Check that quantity could not be negative, zero or float
    """
    ob = OrderBook()
    with pytest.raises(ValueError):
        ob.place_order('1', 10.5, -4, order_type)
    with pytest.raises(ValueError):
        ob.place_order('1', 10.5, 0, order_type)
    with pytest.raises(ValueError):
        ob.place_order('1', 10.5, 4.4, order_type)


@pytest.mark.parametrize('order_type', ['ask', 'bid'])
def test_cancel_order(order_type):
    """
    Check that order cancels correctly
    """
    ob = OrderBook()

    # firstly, place 5 asks and 5 bids with increasing prices
    expected_orders = {'ask': [], 'bid': []}
    for i in range(1, 6):
        for ot in ('ask', 'bid'):
            order = {
                'order_id': f'{ot} {i}',
                'price': i,
                'quantity': random.randint(1, 100)
            }
            ob.place_order(**order, order_type=ot)
            expected_orders[ot].append(order)

    # cancel order
    ob.cancel_order(f'{order_type} 3')
    del expected_orders[order_type][2]
    assert ob.asks == expected_orders['ask']
    assert ob.bids == expected_orders['bid']


@pytest.mark.parametrize('order_type', ['ask', 'bid'])
def test_cancel_non_existing_order(order_type):
    """
    Check that method raises ValueError if order_id does not exist
    (when there are no other orders, and when there are other orders with
    different order_ids)
    """
    ob = OrderBook()
    with pytest.raises(ValueError):
        ob.cancel_order('1')
    ob.place_order('1', 10, 2, order_type)
    with pytest.raises(ValueError):
        ob.cancel_order('2')


@pytest.mark.parametrize('order_type', ['ask', 'bid'])
def test_get_order_info(order_type):
    """
    Check that method returns correct info about an order
    """
    ob = OrderBook()
    order = {
        'order_id': '10',
        'price': random.randint(1, 10),
        'quantity': random.randint(1, 100),
        'order_type': order_type
    }
    ob.place_order(**order)
    assert ob.get_order_info('10') == order


@pytest.mark.parametrize('order_type', ['ask', 'bid'])
def test_get_info_non_existing_order(order_type):
    """
    Check that method raises ValueError if order_id does not exist
    (when there are no other orders, and when there are other orders with
    different order_ids)
    """
    ob = OrderBook()
    with pytest.raises(ValueError):
        ob.get_order_info('1')
    ob.place_order('1', 10, 2, order_type)
    with pytest.raises(ValueError):
        ob.get_order_info('2')


def test_get_market_data_different_prices():
    """
    Check that method returns correct market data if all prices are different
    """
    ob = OrderBook()

    # firstly, place 5 asks and 5 bids with increasing different prices
    expected_market_data = {'asks': [], 'bids': []}
    for i in range(1, 6):
        for order_type in ('ask', 'bid'):
            order = {
                'price': i,
                'quantity': random.randint(1, 100)
            }
            ob.place_order(**order, order_type=order_type,
                           order_id=f'{order_type} {i}')
            expected_market_data[order_type + 's'].append(order)

    assert ob.get_market_data() == expected_market_data


def place_orders_same_price(ob, price, n_orders, order_type):
    """
    Helper function, place n_orders with given price
    into the order_book instance

    :param ob: order_book instance
    :param price: float
    :param n_orders: number of orders with the same price
    :param order_type: 'ask' or 'bid'
    :return: total quantity of the placed orders
    """
    quantity = 0
    for _ in range(n_orders):
        order = {
            'price': price,
            'quantity': random.randint(1, 100)
        }
        quantity += order['quantity']
        ob.place_order(**order, order_type=order_type,
                       order_id=str(random.random()))
    return quantity


@pytest.mark.parametrize('order_type', ['ask', 'bid'])
def test_get_market_data_same_prices(order_type):
    """
    Check that method returns correct market data if all prices are the same
    """
    ob = OrderBook()
    expected_market_data = {'asks': [], 'bids': []}

    # firstly, place 5 orders with the same price
    price = 10
    quantity = place_orders_same_price(ob, price, 5, order_type)
    expected_market_data[order_type + 's'].append({
        'price': price,
        'quantity': quantity
    })

    assert ob.get_market_data() == expected_market_data


def test_get_market_data():
    """
    Check that method returns correct market data (some prices are different,
    some the same; there are both asks and bids; highest price for bids is
    greater than lowest price for asks)
    """
    ob = OrderBook()
    expected_market_data = {'asks': [], 'bids': []}

    # firstly, place 3 asks with the same price
    price = 10
    quantity = place_orders_same_price(ob, price, 3, 'ask')
    expected_market_data['asks'].append({
        'price': price,
        'quantity': quantity
    })
    # then, place 3 bids with the same price
    price = 5
    quantity = place_orders_same_price(ob, price, 3, 'bid')
    expected_market_data['bids'].append({
        'price': price,
        'quantity': quantity
    })
    # then, place 3 asks with the same price (lower than before)
    price = 7
    quantity = place_orders_same_price(ob, price, 3, 'ask')
    expected_market_data['asks'].insert(0, {
        'price': price,
        'quantity': quantity
    })
    # then, place 3 bids with the same price (greater than before)
    price = 8
    quantity = place_orders_same_price(ob, price, 3, 'bid')
    expected_market_data['bids'].append({
        'price': price,
        'quantity': quantity
    })

    assert ob.get_market_data() == expected_market_data


def test_get_empty_market_data():
    """
    Check that method works correctly if there are no orders
    """
    ob = OrderBook()
    assert ob.get_market_data() == {'asks': [], 'bids': []}
