# urls.py - API URL Configuration

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, ReviewViewSet

# Swagger documentation setup
schema_view = get_schema_view(
   openapi.Info(
      title="E-Commerce API",
      default_version='v1',
      description="E-commerce platform API documentation",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@ecommerce.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)  # Handles CRUD for categories
router.register(r'products', ProductViewSet)  # Handles CRUD for products
router.register(r'orders', OrderViewSet)  # Handles order management
router.register(r'order-items', OrderItemViewSet)  # Handles order item details
router.register(r'reviews', ReviewViewSet)  # Handles product reviews

# Define URL patterns for authentication, API endpoints, and documentation
urlpatterns = [
    # JWT Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # API documentation
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-docs'),  # Redoc UI
    
    # Include API routes from the router
    path('', include(router.urls)),
]