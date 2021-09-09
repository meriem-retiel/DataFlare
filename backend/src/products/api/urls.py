from django.urls import path, include
from .views import ProductDetailView,CreateActualSales,ProductListView,ProductActualSales,ProductAdjustedSales,ProductForecastedSales,ProductTable

urlpatterns = [
    path('',ProductListView.as_view()),
    path('<pk>',ProductDetailView.as_view()),
    path('salesActual/<str:pk>/',ProductActualSales),
    path('salesForecasted/<str:pk>/',ProductForecastedSales),
    path('salesAdjusted/<str:pk>/',ProductAdjustedSales),
    path('importsalesActual/',CreateActualSales),

    #path('productTable/<str:pk>/',ProductTable),
]
