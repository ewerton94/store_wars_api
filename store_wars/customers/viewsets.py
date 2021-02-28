import datetime

from rest_framework import viewsets

from .models import *
from .serializers import *


class CustomerViewSet(viewsets.ModelViewSet):
    
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    http_method_names = ['get']
