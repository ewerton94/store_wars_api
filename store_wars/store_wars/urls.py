"""store_wars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from customers.routes import router as customers_router
from products.routes import router as products_router
from rest_framework_swagger.views import get_swagger_view

# Swagger Schema View (Default)
schema_swagger_view = get_swagger_view(title='Store Wars API')

urlpatterns = [
    path('', schema_swagger_view),
    path('admin/', admin.site.urls),
    path('customers/', include(customers_router.urls)),
    path('products/', include(products_router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
