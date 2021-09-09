from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import ForecastedSales,Date, ActualSales, Product
from ..api.serializers import DateSerializer, SalesActualSerializer, SalesForecastedSerializer
#from keras.models import load_model
import joblib
#from pandas import Series
import numpy as np
#from numpy import asarray
#import pandas as pd
from django.templatetags.static import static

@api_view(['GET'])
def PredictionModels(request,pk,model):
        if model == 'RF':
            path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\RF_model.pkl" 
            #load the model
            RF=joblib.load(path)
            #extract last actual predictions
             #order by date id pr date__date value
             #order all sales by date__date
            previous_4_ordered_sales= ActualSales.objects.all().order_by('-date__date')[:4].values('quantity','date__date')      
            # convert quesryset to list
            list_result = [x.get('quantity') for x in previous_4_ordered_sales]#[t-1,t-2,t-3,t-4]
            #reverse list 
            sales = [x for x in reversed(list_result)]#[t-4,t-3,t-2,t-1]
            #reshape list 1D to 2D
            sales_2D = np.reshape(sales, (1,4))
            #predict [[ 3072. , 3475.  ,6405. , 6303.]]=>10953
            unistep = RF.predict(sales_2D)
            #get product instance
            product_instance = Product.objects.get(id=pk)
            print(product_instance)
            #create & get new date instance
            latest_date = previous_4_ordered_sales.values('date__date')[0].get('date__date')
            #to get new date of prediction, add a month
            new_date = add_months(latest_date,1)
            print(new_date)
            date1 = Date(date =datetime.date(2017, 1, 1) )
            #read quantity 
            date1.save()
            date_instance = DateSerializer(date=new_date)
            print(date_instance)
            #serializer= SalesForecastedSerializer(product=product_instance )
            #add to ForecastSales Model
            #serializer.save()
            return Response(unistep) 
import datetime
import calendar

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)