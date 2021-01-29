from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from subscriptions.errors import ProlongingError
from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer
from subscriptions.services.prolong import ProlongSubscription


class SubscriptionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()

    @action(detail=True, methods=['put'])
    def activate(self, request, *args, **kwargs):
        subscription = self.get_object()
        subscription.is_active = True
        subscription.save()
        return Response(status=200)

    def get_queryset(self):
        return super().get_queryset().filter(client=self.request.user)

    def create(self, request, *args, **kwargs):
        if request.user.subscription_set.all().exists():
            operator = ProlongSubscription(subscription=request.user.subscription_set.last())
            try:
                operator.prolong()
                obj = self.serializer_class(operator.new_sub).data
            except ProlongingError:
                return Response(status=status.HTTP_401_UNAUTHORIZED, data=operator.errors)
        else:
            obj = super().create(request, *args, **kwargs)
        return Response(obj, status=status.HTTP_201_CREATED)

