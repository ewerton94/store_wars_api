from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Order, get_multiple_situation
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (permissions.AllowAny,)

    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request, *args, **kwargs):
        r = super().create(request, *args, **kwargs)
        if not all([
            get_multiple_situation(
                item=item.get('quantity'),
                product_id=item.get('product')
                ) for item in request.data.get('items')
                ]):
            return Response(
                {'error': 'Você não pode criar um ítem com rendabilidade baixa'},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        items = r.data.get('items')
        if any([item.get('profitability') == 'bad' for item in items]):
            return Response(
                {'error': 'Você não pode criar um ítem com rendabilidade baixa'},
                status=status.HTTP_406_NOT_ACCEPTABLE
            )
        return r
