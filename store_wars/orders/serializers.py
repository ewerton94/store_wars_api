from customers.serializers import CustomerSerializer
from customers.models import Customer
from products.serializers import ProductSerializer
from products.models import Product
from rest_framework import serializers

from .models import Item, Order


class ItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)

    class Meta:
        model = Item
        fields = ['id', 'product', 'quantity', 'price']

    def to_internal_value(self, data):
        self.fields['product'] = serializers.PrimaryKeyRelatedField(
            queryset=Product.objects.all())
        return super(ItemSerializer, self).to_internal_value(data)


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(many=False)
    items = ItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ["id", 'customer', 'items']

    def to_internal_value(self, data):
        self.fields['customer'] = serializers.PrimaryKeyRelatedField(
            queryset=Customer.objects.all())
        return super(OrderSerializer, self).to_internal_value(data)

    def create_items_from_dict(self, order, items):
        items = []
        for item in items:
            item['order_id'] = order.id
            items.append(Item(**item))
        return items

    def create_items(self, order, items):
        items = self.create_items_from_dict(order, items)
        Item.objects.bulk_create(items)

    def create(self, validated_data):
        order = Order.objects.create(customer=validated_data.get('customer'))
        items = validated_data.pop('items')
        self.create_items(order, items)
        order.refresh_from_db()
        return order

    def update(self, order, validated_data):
        items = validated_data.pop('items')
        for field in validated_data:
            if Order._meta.get_field(field):
                setattr(order, field, validated_data[field])
        order.save()
        Item.objects.filter(order=order).delete()
        self.create_items(order, items)
        order.refresh_from_db()
        return order
