from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from subscriptions.models import Subscription
from subscriptions.serializers import SubscriptionSerializer


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
