from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..models import AdjustedSales, ForecastedSales, Product, ActualSales
from .serializers import ProductSerializer, ProductTableSerializer, SalesActualSerializer, SalesForecastedSerializer,SalesAdjustedSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
import datetime

# Create your views here.
class ProductListView(ListAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer

class ProductDetailView(RetrieveAPIView):
    queryset= ActualSales.objects.all()
    serializer_class= ProductSerializer


#sales actual of a Product with id pk
@api_view(['GET'])
def ProductActualSales(request,pk):
        sales = ActualSales.objects.filter(product=pk,date=datetime.date(2019, 1, 1))
        serializer = SalesActualSerializer(sales,many=True)
        return Response(serializer.data)

#sales forcasted of a Product with id pk
@api_view(['GET'])
def ProductForecastedSales(request,pk):
        sales = ForecastedSales.objects.filter(product=pk)
        serializer = SalesForecastedSerializer(sales,many=True)
        return Response(serializer.data)


#sales adjusted of a Product with id pk
@api_view(['GET'])
def ProductAdjustedSales(request,pk):
        sales = AdjustedSales.objects.filter(product=pk)
        serializer = SalesAdjustedSerializer(sales,many=True)
        return Response(serializer.data)

#Get all sales in one api call
from collections import namedtuple
ProductTable = namedtuple('ProductTable', ('Actuals', 'Forecasted'))

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

        