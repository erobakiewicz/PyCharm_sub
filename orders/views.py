from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from orders.serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(subscription__client=self.request.user)
