from django.urls import path, include
from .views import ProductDetailView,CreateActualSales,ProductListView,ProductActualSales,ProductAdjustedSales

urlpatterns = [
    #validated
    path('',ProductListView.as_view()),
    #not yet
    path('<pk>',ProductDetailView.as_view()),
    #validated
    path('salesActual/<str:pk>/',ProductActualSales),
    #validated
    path('salesAdjusted/<str:pk>/',ProductAdjustedSales),
    #not yet
    path('importsalesActual/',CreateActualSales),

    #path('productTable/<str:pk>/',ProductTable),
]
