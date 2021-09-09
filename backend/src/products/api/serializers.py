from django.db.models import fields
from rest_framework import serializers
from ..models import AdjustedSales, ForecastedSales, Product, ActualSales, Date 

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model= Product
        fields = ('dci','dosage','forme','designation')


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Date  
        fields = ('date',)




class SalesForecastedSerializer(serializers.ModelSerializer):
    #date = serializers.DateField(source="date.date", read_only=True)
    date = DateSerializer()
    product = ProductSerializer()

    class Meta:
        model= ForecastedSales 
        fields = ('product','quantity','date')

class SalesAdjustedSerializer(serializers.ModelSerializer):
    #date = serializers.DateField(source="date.date", read_only=True)
    date = DateSerializer()
    product = ProductSerializer()
    class Meta:
        model= AdjustedSales 
        fields = ('product','quantity','date')

class SalesActualSerializer(serializers.ModelSerializer):
    #date= serializers.StringRelatedField(read_only=True)
    #date = serializers.DateField(source="date.date", read_only=True)
    date = DateSerializer()
    product = ProductSerializer()
    class Meta:
        model= ActualSales 
        fields = ('product','quantity','date')
    #def create(self, validated_data):
        """
        Create and return a new `ActualSale` instance, given the validated data.
        """
        #create date if not exist
        #return ActualSales.objects.create(**validated_data)

#class ProductTableSerializer(serializers.Serializer):
    #Actuals = SalesActualSerializer(many=True)
    #Forecasted = SalesForecastedSerializer(many=True)