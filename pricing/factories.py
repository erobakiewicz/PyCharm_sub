import factory.fuzzy

from .constants import Countries
from .models import Pricing
from subscriptions.constants import SpecialOffers, UserTypes


class PricingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Pricing

    offer_type = factory.fuzzy.FuzzyChoice([a_tuple[0] for a_tuple in SpecialOffers.Choices])
    user_type = factory.fuzzy.FuzzyChoice([a_tuple[0] for a_tuple in UserTypes.Choices])
    price_monthly = factory.fuzzy.FuzzyDecimal(50.00, 150.00)
    country = factory.fuzzy.FuzzyChoice([a_tuple[0] for a_tuple in Countries.Choices])
