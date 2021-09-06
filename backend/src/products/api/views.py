from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..models import Product, ActualSales
from .serializers import ProductSerializer, SalesActualSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.
class ProductListView(ListAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer

class ProductDetailView(RetrieveAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer

#sales actual of a Product with id pk
@api_view(['GET'])
def ProductActualSales(request,pk):
        sales = ActualSales.objects.filter(product=pk)
        serializer = SalesActualSerializer(sales,many=True)
        return Response(serializer.data)
#def setUpTestData(self):
 #       Product.objects.create(dci='asperine')
  #      prod = Product.objects.get(id=1)
   #     expected_object_name = f'{prod.dci}'
    #    self.assertEqual(expected_object_name, 'first dci')

        