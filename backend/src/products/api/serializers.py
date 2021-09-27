from django.db.models import fields
from rest_framework import serializers
from ..models import AdjustedSales, ForecastedSales, Product, ActualSales, Date 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = ('id','dci','dosage','forme','designation')

class SalesActualSerializer(serializers.ModelSerializer):
    #date= serializers.StringRelatedField(read_only=True)
    date = serializers.DateField(source="date.date", read_only=True)
    class Meta:
        model= ActualSales 
        fields = ('product','quantity','date')

class SalesForecastedSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="date.date", read_only=True)

    class Meta:
        model= ForecastedSales 
        fields = ('product','quantity','date')

class SalesAdjustedSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="date.date", read_only=True)

    class Meta:
        model= AdjustedSales 
        fields = ('product','quantity','date')


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Date  
        fields = ('quantity','product','date')

class ProductTableSerializer(serializers.Serializer):
    Actuals = SalesActualSerializer(many=True)
    Forecasted = SalesForecastedSerializer(many=True)