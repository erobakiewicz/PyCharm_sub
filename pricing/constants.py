from decimal import Decimal


class Countries:
    POLAND = 'Poland'
    USA = 'USA'
    ESTONIA = 'Estonia'

    Choices = (
        (POLAND, 'Poland'),
        (USA, 'USA'),
        (ESTONIA, 'ESTONIA'),
    )

    TAXES = {
        POLAND: Decimal('0.23'),
        USA: Decimal('0.19'),
        ESTONIA: Decimal('0.17'),
    }
