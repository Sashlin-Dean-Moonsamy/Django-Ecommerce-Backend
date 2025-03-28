from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import filters
from django.core.cache import cache
from django.db.models import Count, Avg
from .models import Category, Product, Order, OrderItem, Review
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, ReviewSerializer
from .cach_keys import POPULAR_PRODUCTS_KEY_CACHE_KEY

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
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = ['name']  # Example of allowing filtering by name
    ordering_fields = ['name']  # Example of ordering categories by name
    ordering = ['name']  # Default ordering
    # permission_classes = [IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['GET'], url_path='popular')
    def popular_products(self, request):
        cache_key = POPULAR_PRODUCTS_KEY_CACHE_KEY

        # Check if popular products are cached
        cached_data = cache.get(cache_key)
        if not cached_data:
            # Annotate each product with total sales (from OrderItem) and average review rating
            products = Product.objects.annotate(
                total_sales=Count('orderitem'),  # Count how many times a product has been ordered (via OrderItem)
                avg_rating=Avg('reviews__rating')  # Average review rating for the product
            ).order_by('-total_sales', '-avg_rating')[:10]  # Sort by total_sales first, then avg_rating
            
            # Serialize and cache the result
            cached_data = ProductSerializer(products, many=True, context={"request": request}).data
            cache.set(cache_key, cached_data, timeout=3600)  # Cache for 1 hour
        
        return Response(cached_data)


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