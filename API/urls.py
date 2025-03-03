from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from .views import CategoryViewSet, ProductViewSet, OrderViewSet, OrderItemViewSet, ReviewViewSet

# Documentation setup
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

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order-items', OrderItemViewSet)
router.register(r'reviews', ReviewViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('docs/', schema_view.as_view(), name='swagger-docs'),  # Swagger Docs
    path('', include(router.urls)),

]
