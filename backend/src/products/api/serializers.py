from django.db.models import fields
from rest_framework import serializers
from ..models import AdjustedSales, ForecastedSales, Product, ActualSales, Date 
import logging
class ProductSerializer(serializers.ModelSerializer):
    actual = serializers.StringRelatedField(many=True)#bring all sales of product
    forecast = serializers.StringRelatedField(many=True)
    adjusted = serializers.StringRelatedField(many=True)
    class Meta:
        model= Product
        fields = ('dci','dosage','forme','designation')

class SalesActualSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="date.date", read_only=True)
    product = serializers.CharField(source = "product.id_prod",read_only=True)
    class Meta:
        model= ActualSales 
        fields = ('id_actual','product','date','quantity')

class SalesAdjustedSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="date.date", read_only=True)
    product = serializers.CharField(source = "product.id_prod",read_only=True)
    class Meta:
        model= AdjustedSales 
        fields = ('product','date', 'quantity')

class SalesForecastedSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="date.date", read_only=True)
    product = serializers.CharField(source = "product.id_prod",read_only=True)
    class Meta:
        model= ForecastedSales 
        fields = ('id_forcast','date','quantity', 'model_name', 'horizon')

class DateSerializer(serializers.ModelSerializer):
    actualsale= serializers.StringRelatedField(many=True)#bring all sales of date
    forecastsale = serializers.StringRelatedField(many=True)
    adjustedsale = serializers.StringRelatedField(many=True)
    class Meta:
        model= Date  
        fields = ('date',)##added id

#class ProductTableSerializer(serializers.Serializer):
    #Actuals = SalesActualSerializer(many=True)
    #Forecasted = SalesForecastedSerializer(many=True)