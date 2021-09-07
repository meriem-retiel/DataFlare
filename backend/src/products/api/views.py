from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..models import AdjustedSales, ForecastedSales, Product, ActualSales
from .serializers import ProductSerializer, ProductTableSerializer, SalesActualSerializer, SalesForecastedSerializer,SalesAdjustedSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# Create your views here.
class ProductListView(ListAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer

class ProductDetailView(RetrieveAPIView):
    queryset= Product.objects.all()
    serializer_class= ProductSerializer

#sales actual of a Product with id pk
@api_view(['GET','Post'])
def ProductActualSales(request,pk):
    if request.method == 'Get':
            sales = ActualSales.objects.filter(product=pk)
            serializer = SalesActualSerializer(sales,many=True)
            return Response(serializer.data)
    elif request.method == 'Post':
        serializer = SalesActualSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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
##########################
#sales forcasted of a Product with id pk
@api_view(['GET'])
#add later Model names so need specify model_name to get its prediction
def ProductForecastedSales(request,pk):
        sales = ForecastedSales.objects.filter(product=pk)
        serializer = SalesForecastedSerializer(sales,many=True)
        return Response(serializer.data)


#when user adjust in table
@api_view(["GET"])
def AddAdjustedSales(request):
#Create a sales instance from POST data 
        a = AdjustedSales(request.Post)
#save it in model
        a.save()

#when user import data
@api_view(["GET"])
def AddActualSales(request):
#Create a sales instance from POST data 
        a = ActualSales(request.Post)
#save it in model
        a.save()
#this function shouldnt run with request but auto
def ProductPrediction():  
          #all product
          
            return()            