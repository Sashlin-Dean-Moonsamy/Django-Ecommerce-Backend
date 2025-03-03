from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Category, Product, Order, Review

class APITestCases(APITestCase):
    
    def setUp(self):
        """Set up test user and initial data."""
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(name='Laptop', category=self.category, price=1000.00, stock=10)
        self.order = Order.objects.create(user=self.user, total_price=1000.00, status='pending')
        self.review = Review.objects.create(user=self.user, product=self.product, rating=5, comment='Great product!')
        
        # Obtain JWT token
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
    
    def test_get_categories(self):
        """Test retrieving category list."""
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_products(self):
        """Test retrieving product list."""
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_order(self):
        """Test creating an order."""
        data = {
            "user": self.user.id,
            "total_price": 500.00,
            "status": "pending"
        }
        response = self.client.post('/orders/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_review(self):
        """Test creating a product review."""
        data = {
            "user": self.user.id,
            "product": self.product.id,
            "rating": 4,
            "comment": "Good quality!"
        }
        response = self.client.post('/reviews/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_invalid_token_access(self):
        """Test accessing an endpoint without authentication."""
        self.client.credentials()  # Remove auth headers
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
