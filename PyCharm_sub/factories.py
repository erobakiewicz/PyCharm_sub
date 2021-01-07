import factory
from django.contrib.auth.models import User

from subscriptions.models import Subscription


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username{0}'.format(n))
    first_name = factory.Sequence(lambda n: 'fname{0}'.format(n))
    last_model = factory.Sequence(lambda n: 'lname{0}'.format(n))
    email = factory.Sequence(lambda n: 'mail{0}@mail.com'.format(n))


class SubscriptionFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Subscription

    price = factory.Iterator(['20', '30', '50'], cycle=False)
    user = factory.SubFactory(UserFactory)
