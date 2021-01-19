class OrderStatus:
    PAID = 'paid'
    IN_PROGRESS = 'in progress'
    NOT_PAID = 'not paid'
    DECLINED = 'declined'

    Choices = (
        (PAID, 'paid'),
        (IN_PROGRESS, 'in progress'),
        (NOT_PAID, 'not paid'),
        (DECLINED, 'declined'),
    )
