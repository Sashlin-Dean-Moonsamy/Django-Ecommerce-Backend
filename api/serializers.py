# serializers.py
from rest_framework import serializers
from .models import Category, Product, Order, OrderItem, Review

class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    Includes a nested CategorySerializer to display category details.
    """
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'date_time_added', 'updated_at']


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)  # 🔹 Include products in category

    """
    Serializer for the Category model.
    Serializes the 'id', 'name', and 'description' fields.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'products']



class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.
    Includes a nested ProductSerializer to display product details.
    """
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'quantity', 'price']

class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.
    - Uses StringRelatedField for the user to return the username.
    - Uses OrderItemSerializer as a nested serializer to display order items.
    """
    user = serializers.StringRelatedField()
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'products', 'total_price', 'status', 'order_date']

class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.
    - Uses StringRelatedField for the user to return the username.
    - Uses ProductSerializer as a nested serializer to display product details.
    """
    user = serializers.StringRelatedField()
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']
