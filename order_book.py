import bisect
import typing


class OrderBook:
    def __init__(self):
        # all orders (sorted by price, first bids then asks)
        self.orders: typing.List[typing.Dict] = []
        # list of prices (in the same order as self.orders)
        self.prices: typing.List[float] = []

    def place_order(
            self,
            order_id: str,
            price: float,
            quantity: int,
            order_type: str
    ) -> typing.NoReturn:
        """
        Place an order into order book (self.orders)

        :param order_id: unique id of an order
        :param price: order price
        :param quantity: order quantity
        :param order_type: 'ask' or 'bid'
        :return: None
        """
        if self.order_id_exists(order_id):
            raise ValueError(f'Order_id \'{order_id}\' already exists, '
                             f'please give another one')

        if order_type not in ('ask', 'bid'):
            raise ValueError(f'Unknown order_type \'{order_type}\', only '
                             f'\'ask\' and \'bid\' are possible')

        index = bisect.bisect(self.prices, price)
        self.orders.insert(index, {
            'order_id': order_id,
            'price': price,
            'quantity': quantity,
            'order_type': order_type
        })
        self.prices.insert(index, price)

    def order_id_exists(self, order_id: str) -> bool:
        """
        Tells if order_id already exists in order_book (self.orders)

        :param order_id: new order id
        :return: True if new order_if already exists else False
        """
        for order in self.orders:
            if order['order_id'] == order_id:
                return True
        return False

    def cancel_order(self, order_id: str) -> None:
        """
        Cancels an existing order

        :param order_id: existing order id
        :return: None
        """
        for i, order in enumerate(self.orders):
            if order['order_id'] == order_id:
                del self.orders[i]
                del self.prices[i]
                return
        raise ValueError(f'Order_id \'{order_id}\' not found')

    def get_order_info(self, order_id: str) -> typing.Dict:
        """
        Returns info about an order with given order_id

        :param order_id: existing order id
        :return: dict with info about the order
        """
        for order in self.orders:
            if order['order_id'] == order_id:
                return order
        raise ValueError(f'Order_id \'{order_id}\' not found')
