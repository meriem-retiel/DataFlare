from django.urls import path, include
from .views import ProductDetailView,ProductListView,ProductActualSales,ProductForecastedSales,ProductTable

urlpatterns = [
    path('',ProductListView.as_view()),
    path('<pk>',ProductDetailView.as_view()),
    path('salesActual/<str:pk>/',ProductActualSales),
    path('salesForecasted/<str:pk>/',ProductForecastedSales),
    path('productTable/<str:pk>/',ProductTable),
]