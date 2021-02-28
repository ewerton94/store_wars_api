from rest_framework import viewsets
from rest_framework.routers import DefaultRouter

from . import viewsets

router = DefaultRouter()
router.register(r'', viewsets.CustomerViewSet)
