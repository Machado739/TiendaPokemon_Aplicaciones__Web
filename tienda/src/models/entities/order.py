class Order:
    def __init__(self, order_id, user_id, order_date, total_amount, payment_method_id):
        self.order_id = order_id
        self.user_id = user_id
        self.order_date = order_date
        self.total_amount = total_amount
        self.payment_method_id = payment_method_id