# serializers.py
from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, Review
from django.contrib.auth.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'image', 'date_time_added', 'updated_at']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'total_price', 'status', 'order_date']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']
