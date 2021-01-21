import typing


class OrderBook:
    def __init__(self):
        self.asks: typing.List[typing.Dict] = [] # all asks (sorted by price)
        self.bids: typing.List[typing.Dict] = [] # all bids (sorted by price)

    def place_order(
            self,
            order_id: str,
            price: float,
            quantity: int,
            order_type: str
    ) -> typing.NoReturn:
        """
        Place an order into order book (self.asks or self.bids)

        :param order_id: unique id of an order
        :param price: order price (positive float)
        :param quantity: order quantity
        :param order_type: 'ask' or 'bid'
        :return: None
        """
        if self.order_id_exists(order_id):
            raise ValueError(f'Order_id \'{order_id}\' already exists, '
                             f'please give another one')
        if price <= 0:
            raise ValueError(f'Price should be a positive number, but '
                             f'\'{price}\' was given')
        if quantity <= 0 or not isinstance(quantity, int):
            raise ValueError(f'Quantity should be a positive integer, but '
                             f'\'{quantity}\' was given')

        order = {
            'order_id': order_id,
            'price': price,
            'quantity': quantity
        }
        if order_type == 'ask':
            self.insert_order(self.asks, order)
        elif order_type == 'bid':
            self.insert_order(self.bids, order)
        else:
            raise ValueError(f'Unknown order_type \'{order_type}\', only '
                             f'\'ask\' and \'bid\' are possible')

    def insert_order(self, orders: typing.List[typing.Dict],
                     new_order: typing.Dict) -> typing.NoReturn:
        """
        Insert new_order into the list of orders, so that prices remain sorted

        :param orders: self.asks or self.bids
        :param new_order: new order
        :return: None
        """
        for i, order in enumerate(orders):
            if order['price'] >= new_order['price']:
                orders.insert(i, new_order)
                return

        # if all the prices in the orders list are lower than new_order's price,
        # insert new_order in the end of the orders list
        orders.insert(len(orders), new_order)

    def order_id_exists(self, order_id: str) -> bool:
        """
        Tells if order_id already exists in order_book (self.asks or self.bids)

        :param order_id: new order id
        :return: True if new order_if already exists else False
        """
        for order in self.asks + self.bids:
            if order['order_id'] == order_id:
                return True
        return False

    def cancel_order(self, order_id: str) -> typing.NoReturn:
        """
        Cancels an existing order

        :param order_id: existing order id
        :return: None
        """
        for i, order in enumerate(self.asks):
            if order['order_id'] == order_id:
                del self.asks[i]
                return
        for i, order in enumerate(self.bids):
            if order['order_id'] == order_id:
                del self.bids[i]
                return
        raise ValueError(f'Order_id \'{order_id}\' not found')

    def get_order_info(self, order_id: str) -> typing.Dict:
        """
        Returns info about an order with given order_id

        :param order_id: existing order id
        :return: dict with info about the order
        """
        for order in self.asks + self.bids:
            if order['order_id'] == order_id:
                return order
        raise ValueError(f'Order_id \'{order_id}\' not found')
