from datetime import datetime

import factory
from django.contrib.auth.models import User
import factory
import factory.fuzzy
from subscriptions.models import Subscription


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username{0}'.format(n))
    first_name = factory.Sequence(lambda n: 'fname{0}'.format(n))
    last_name = factory.Sequence(lambda n: 'lname{0}'.format(n))
    email = factory.Sequence(lambda n: 'mail{0}@mail.com'.format(n))


class SubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Subscription

    sub_period = factory.Sequence(lambda n: '2022-02-02'.format(n))
    is_active = factory.Faker("pybool")
    user_type = factory.fuzzy.FuzzyChoice(['individual','business'])
    billing_type = factory.fuzzy.FuzzyChoice(['monthly','yearly'])
    special_offers = factory.fuzzy.FuzzyChoice(['student','classroom_assistant'])
    sub_quantity = factory.fuzzy.FuzzyInteger(1)
    us_tax = factory.Faker("pybool")
    price = factory.fuzzy.FuzzyDecimal(20.0,20.0)
    client = factory.SubFactory(UserFactory)
