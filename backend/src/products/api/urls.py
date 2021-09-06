from django.urls import path, include
from .views import ProductDetailView,ProductListView,ProductActualSales

urlpatterns = [
    path('',ProductListView.as_view()),
    path('<pk>',ProductDetailView.as_view()),
    path('sales/<str:pk>/',ProductActualSales)
]