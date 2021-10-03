from django.db.models import fields
from rest_framework import serializers
from ..models import AdjustedSales, ForecastedSales, Product, ActualSales, Date 
import logging
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = ('id','dci','dosage','forme','designation')



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
        fields = ('date',)

class SalesActualSerializer(serializers.ModelSerializer):
    #date= serializers.StringRelatedField(read_only=True)
    date = DateSerializer()
    product=ProductSerializer()
    class Meta:
        model= ActualSales 
        fields = ('product','quantity','date')
    def create(self,validated_data):
        product_data=validated_data.pop('product')
        date_data=validated_data.pop('date')
        quantity_data=validated_data.pop('quantity')
        product,created=Product.objects.get_or_create(**product_data)
        date=Date.objects.create(**date_data)
        actualsales=ActualSales.objects.create(date=date,product=product,quantity=quantity_data)
        return actualsales

class ProductTableSerializer(serializers.Serializer):
    Actuals = SalesActualSerializer(many=True)
    Forecasted = SalesForecastedSerializer(many=True)