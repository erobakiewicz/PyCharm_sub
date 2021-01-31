import factory.fuzzy
from django.utils import timezone

from PyCharm_sub.factories import SubscriptionFactory
from .constants import OrderStatus
from .models import Order


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    subscription = factory.SubFactory(SubscriptionFactory)
    order_status = factory.fuzzy.FuzzyChoice([OrderStatus.PAID,
                                              OrderStatus.IN_PROGRESS,
                                              OrderStatus.NOT_PAID,
                                              OrderStatus.DECLINED])
    created = timezone.now()
    updated = timezone.now()
    email = factory.Sequence(lambda n: 'person{}@example.com'.format(n))
    price = factory.fuzzy.FuzzyDecimal(100.00)
