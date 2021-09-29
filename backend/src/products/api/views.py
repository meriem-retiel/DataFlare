from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from ..models import Date,AdjustedSales, ForecastedSales, Product, ActualSales
from .serializers import DateSerializer, ProductSerializer, SalesActualSerializer, SalesForecastedSerializer,SalesAdjustedSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
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
        sales = ActualSales.objects.filter(
        product=pk#,date__date__range=[datetime.date(yearD, monthD, 1),datetime.date(yearF, monthF, 1)]
        )
        serializer = SalesActualSerializer(sales,many=True)
        return Response(serializer.data)
#for now case try save one element outta many
@api_view(['Post'])
def CreateActualSales(request):   
        #####use serializers to create json, models return strings
        ################back to first plan
        req_data = request.data 
        date1 = Date(date =datetime.date(2017, 1, 1) )
        serializer = SalesActualSerializer(data=request.data, many=True)
        serializer.save()#want call create
        
        print(req_data)
        date= req_data[1]['date']
        #create & save date instance for test
        date1 = Date(date =datetime.date(2017, 1, 1) )
        #read quantity 
        date1.save()
        quantity1= req_data[1]['quantity']
        #call product object with id prod1
        prod1= req_data[1]['product']
        product1 = Product.objects.get(id=prod1)
        #needs all 3 as entry
        print(product1) 
        sale1 = ActualSales.objects.create(quantity= quantity1, product= product1 , date= date1)
        #sale1.save()
        #print(ActualSales.objects.all())
        print('actualsales modele return sale1')
        print(sale1)
        #dict_sale = dict()
        import json
        #json.dumps(dict_sale)
        serializer = SalesActualSerializer(data=sale1, many=True)
        #print(serializer)
        #print(ActualSales.objects.get(date= '2017-01-01'))
        #date_object= Date.objects.get(date=date1)
        #print(date_object)
        #print('date_object')
        #print(date_object.iddate)
        #print('date_object access attribute id')
        #print(req_data[1]['date'])
        #print(req_data)
        #print("see what request data give to take date")
        #check if date ser must exist before sale ser
        #if serializer.is_valid():
            #date_serializer = DateSerializer(data = date1)#!!!!!
         #   print(serializer)
            #serializer.save()
            #if date_serializer.is_valid():
              #print("date serializer creation")      
              #date_serializer.save()
              #serializer.save()
            
          #  print("outta if")


           # return Response(serializer.data, status=status.HTTP_201_CREATED)
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
#################

#when user adjust in table
@api_view(["POST"])
def AddAdjustedSales(request):
#Create a sales instance from POST data 
        a = AdjustedSales(request.Post)
#save it in model
        a.save()
#when user import data
#def AddActualSales(request):
#Create a sales instance from POST data 
#           