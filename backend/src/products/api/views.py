from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..models import Product
from .serializers import ProductSerializer
# Create your views here.

class ProductListView(ListAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer

class ProductDetailView(RetrieveAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer