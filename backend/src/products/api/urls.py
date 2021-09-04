from django.urls import path, include
from .views import ProductDetailView,ProductListView

urlpatterns = [
    path('',ProductListView.as_view()),
    path('<pk>',ProductDetailView.as_view())
]