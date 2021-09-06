from rest_framework import serializers
from ..models import ForecastedSales, Product, ActualSales, Date 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = ('dci','dosage','forme','designation')

class SalesActualSerializer(serializers.ModelSerializer):
    class Meta:
        model= ActualSales 
        fields = ('quantity','product','date')

class SalesForecastedSerializer(serializers.ModelSerializer):
    class Meta:
        model= ForecastedSales 
        fields = ('quantity','product','date')

class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Date  
        fields = ('quantity','product','date')

class ProductTableSerializer(serializers.Serializer):
    Actuals = SalesActualSerializer(many=True)
    Forecasted = SalesForecastedSerializer(many=True)