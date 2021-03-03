from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.AllowAny,)

    http_method_names = ['get', 'post', 'put']

    def create(self, request, *args, **kwargs):
        r = super().create(request, *args, **kwargs)
        items = r.data.get('items')
        if any([item.get('profitability') == 'bad' for item in items]):
            return Response(
                'Você não pode criar um ítem com rendabilidade baixa',
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        return r
