class PaymentMethod:
    def __init__(self, payment_method_id, user_id, payment_type, card_number, expiration_date, cvv):
        self.payment_method_id = payment_method_id
        self.user_id = user_id
        self.payment_type = payment_type
        self.card_number = card_number
        self.expiration_date = expiration_date
        self.cvv = cvv