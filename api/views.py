from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import Count, Avg
from .models import Category, Product, Order, OrderItem, Review
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, ReviewSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.prefetch_related('products').all()  # Optimize query to get category and related products
                                                                    # loads categories and the producuts from database
                                                                    # usually if you just say .all() it will return catagories and catagory.products.all 
                                                                    # would make a seperate query to database. Now it loads data about products as well 
                                                                    # so a second query does not need to be made
    serializer_class = CategorySerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    cache_key = "popular_products"
    # permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['GET'], url_path='popular')
    def popular_products(self, request):
        
        # Check if popular products are cached
        cached_data = cache.get(self.cache_key)
        if not cached_data:
            # Annotate each product with total sales (from OrderItem) and average review rating
            products = Product.objects.annotate(
                total_sales=Count('orderitem'),  # Count how many times a product has been ordered (via OrderItem)
                avg_rating=Avg('reviews__rating')  # Average review rating for the product
            ).order_by('-total_sales', '-avg_rating')[:10]  # Sort by total_sales first, then avg_rating
            
            # Serialize and cache the result
            cached_data = ProductSerializer(products, many=True, context={"request": request}).data
            cache.set(self.cache_key, cached_data, timeout=3600)  # Cache for 1 hour
        
        return Response(cached_data)
    
    def perform_create(self, serializer):
        """ Override to clear cache when a new product is added """
        super().perform_create(serializer)
        cache.delete(self.cache_key)  # Invalidate cache when a new product is added

    def perform_destroy(self, instance):
        """ Override to clear cache when a product is deleted """
        cache.delete(self.cache_key)  # Invalidate cache when a product is deleted
        super().perform_destroy(instance)

    def perform_update(self, serializer):
        """ Override to clear cache when a product is updated, including image change """
        super().perform_update(serializer)
        cache.delete(self.cache_key)  # Invalidate cache when product (or image) is updated
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows order items to be viewed or edited.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reviews to be viewed or edited.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]