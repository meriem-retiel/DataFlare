from django.db.models import fields
from rest_framework import serializers
from ..models import AdjustedSales, ForecastedSales, Product, ActualSales, Date 

class ProductSerializer(serializers.ModelSerializer):
    actual = serializers.StringRelatedField(many=True)#bring all sales of product
    forecast = serializers.StringRelatedField(many=True)
    #adjusted = serializers.StringRelatedField(many=True)
    class Meta:
        model= Product
        fields = ('id_prod','dci','dosage','forme','designation')


class DateSerializer(serializers.ModelSerializer):
    actualsale= serializers.StringRelatedField(many=True)#bring all sales of date
    forecastsale = serializers.StringRelatedField(many=True)
    class Meta:
        model= Date  
        fields = ('id_date','date','actualsale')##added id

class SalesActualSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="date.date", read_only=True)
    #date = DateSerializer()
    product = ProductSerializer()
    class Meta:
        model= ActualSales 
        fields = '__all__'

class SalesAdjustedSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="date.date", read_only=True)
    #date = DateSerializer()
    #product = ProductSerializer()
    class Meta:
        model= AdjustedSales 
        fields = ('product','quantity','date')

class SalesForecastedSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source="date.date", read_only=True)
    #product = ProductSerializer(source='Product')
    #["{  "product": 1, "quantity": 7121, "date": "2021-02-01","model_name": "RF"  }"..]
    class Meta:
        model= ForecastedSales 
        fields = ('product','quantity','date','model_name')


#class ProductTableSerializer(serializers.Serializer):
    #Actuals = SalesActualSerializer(many=True)
    #Forecasted = SalesForecastedSerializer(many=True)