from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..models import ForecastedSales, Product, ActualSales
from .serializers import ProductSerializer, ProductTableSerializer, SalesActualSerializer, SalesForecastedSerializer
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

#sales actual of a Product with id pk
@api_view(['GET'])
def ProductForecastedSales(request,pk):
        sales = ForecastedSales.objects.filter(product=pk)
        serializer = SalesForecastedSerializer(sales,many=True)
        return Response(serializer.data)

#all sales pf a product in a nested serilized reponses
from collections import namedtuple
ProductTable = namedtuple('ProductTable', ('Actuals', 'Forecasted'))

def Actuals(pk):
        sales = ActualSales.objects.filter(product=pk)
        serializer = SalesActualSerializer(sales,many=True)
        return serializer.data
def Forcasted(pk):
        sales = ForecastedSales.objects.filter(product=pk)
        serializer = SalesForecastedSerializer(sales,many=True)
        return serializer.data

@api_view(['GET'])
def ProductTable(request,pk):
        sales = ActualSales.objects.filter(product=pk)
        serializer1 = SalesActualSerializer(sales,many=True)
        Actual = serializer1.data
        ###########
        sales = ForecastedSales.objects.filter(product=pk)
        serializer2 = SalesForecastedSerializer(sales,many=True)
        Forcast = serializer2.data 
        ##########
        ProductData = ProductTable(
            #Actuals =SalesActualSerializer.objects.filter(product=pk),
            Actuals = Actual,
            Forecasted = Forcast,
            #Forcasted =SalesForecastedSerializer.objects.filter(product=pk),
        )
        serializer = ProductTableSerializer(ProductData,context={"request": request})
        return Response(serializer.data)
#def setUpTestData(self):
 #       Product.objects.create(dci='asperine')
  #      prod = Product.objects.get(id=1)
   #     expected_object_name = f'{prod.dci}'
    #    self.assertEqual(expected_object_name, 'first dci')

        