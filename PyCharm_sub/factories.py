import factory.fuzzy
from django.contrib.auth.models import User
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

    date_created = factory.Sequence(lambda n: '2022-02-02'.format(n))
    is_active = factory.Faker("pybool")
    user_type = factory.fuzzy.FuzzyChoice(['individual','business'])
    billing_type = factory.fuzzy.FuzzyChoice(['monthly','yearly'])
    special_offers = factory.fuzzy.FuzzyChoice(['student','classroom_assistant'])
    client = factory.SubFactory(UserFactory)
