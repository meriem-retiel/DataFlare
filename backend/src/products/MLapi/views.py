from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import ForecastedSales,Date, ActualSales, Product
from ..api.serializers import DateSerializer, ProductSerializer, SalesActualSerializer, SalesForecastedSerializer
#from keras.models import load_model
from keras.models import load_model
import joblib
from pandas import Series
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
            print(sales_2D)#[[ 4545  5000 30000 20000]]
            #predict Quantity test[[ 3072. , 3475.  ,6405. , 6303.]]=>10953
            unistep = RF.predict(sales_2D)
            #######save prediction in forecastSales
            #1--get product instance & serialize
            product_instance = Product.objects.get(id=pk)
            print(product_instance)
            product_serializer = ProductSerializer(product_instance)
            #-2 create new date instance
            latest_date = previous_4_ordered_sales.values('date__date')[0].get('date__date')
            #to get new date of prediction, add a month
            new_date = add_months(latest_date,1)
            date_instance = Date.objects.create(date =new_date)
            #serialize it to send it
            date_serializer = DateSerializer(date_instance)
            #serializer= SalesForecastedSerializer(product=product_serializer, date=date_serializer,quantity= unistep )
            #print(serializer)

            #add to ForecastSales Model
            #serializer.save()
        
            return Response([int(unistep)]) 
        elif model == "MLP":
            path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\MLP_model.h5" 
            MLP = load_model(path)
            #extract last actual predictions
             #order by date id pr date__date value
             #order all sales by date__date
            previous_4_ordered_sales= ActualSales.objects.all().order_by('-date__date')[:4].values('quantity','date__date')      
            # convert quesryset to list
            list_result = [x.get('quantity') for x in previous_4_ordered_sales]#[t-1,t-2,t-3,t-4]
            #reverse list 
            sales = [x for x in reversed(list_result)]#[t-4,t-3,t-2,t-1]
            #reshape list 1D to 2D
            sales_3D = np.reshape(sales, (1, 1,4))#!recheck changed it to take only 4
            print(sales_3D)#[[[ 4545  5000 30000 20000]]]
            unistep_prediction = MLP.predict(sales_3D,verbose=0)###prob
            print(unistep_prediction)
            return Response(int(unistep_prediction))
        elif model =="LSTM" :
            #loading model & scaler!!path to change
            path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\LSTM_model.h5" 
            scaler_path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\lstm_scaler.pkl" 
            LSTM = load_model(path)
            scaler = joblib.load(scaler_path)
            #extracting last 5 actual sales to predict 6th
            previous_6_sales= ActualSales.objects.all().order_by('-date__date')[:6].values('quantity','date__date')      
            # convert quesryset to list
            list_result = [x.get('quantity') for x in previous_6_sales]#[t-1,t-2,t-3,t-4,t-5,t-6]
            #reverse list 
            sales = [x for x in reversed(list_result)]#[t-6,t-5,t-4,t-3,t-2,t-1]
            #differencing
            sales_diff = difference(sales,1)#gives list 
            #scaling 
            sales=np.array(sales_diff).reshape(-1, len(sales_diff))#FROM LIST TO ARRAY 2D
            print(len(sales_diff))
            sales_scaled = scaler.transform(sales.reshape(sales.shape[0], sales.shape[1]))
           #Predicting new value
            X = sales_scaled[0, 0:-1]
            X_3D = X.reshape(1, len(X), 1)
            print(X_3D)#[[[1.23028088e-01][1.63524432e-03][2.36263948e+00]]]
            pred = LSTM.predict(X_3D, batch_size=1)
            #inverse scale
            pred = invert_scale(scaler, X, pred)#-16294.901620864866
            ## invert differenced(requires previous value only) 
            pred = pred + list_result[0]#!!!!logic problm
            print(list_result[0])
            return Response(int(pred))
        else:            
            return Response("No such model")
import datetime
import calendar

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def difference(sales_data, interval=1):
    diff = list()
    for i in range(interval, len(sales_data)):
        value = sales_data[i] - sales_data[i - interval]
        diff.append(value)
    return Series(diff)

# inverse scaling for a forecasted value
def invert_scale(scaler, X, yhat):
	new_row = [x for x in X] + [yhat]
	array = np.array(new_row)
	array = array.reshape(1, len(array))
	inverted = scaler.inverse_transform(array)
	return inverted[0, -1]

