from datetime import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from ..models import ForecastedSales,Date, ActualSales, Product
from ..api.serializers import DateSerializer, ProductSerializer, SalesActualSerializer, SalesForecastedSerializer
from django.templatetags.static import static
from keras.models import load_model
import joblib
from pandas import Series
import numpy as np

from .ML_Models.RF import RF_Training, RF_predictions
from .ML_Models.MLP import MLP_Training, MLP_predictions
from .ML_Models.LSTM import LSTM_Training, LSTM_predictions

@api_view(['GET'])
def Prediction_Visualization(request,pk,model,h):
    if model == 'RF':
        if h == '1':
            sales = ForecastedSales.objects.filter(product=pk,model_name=model)
            serializer = SalesForecastedSerializer(sales,many=True)
            return Response(serializer.data)
            
        elif h =='6':
            return Response(0)
        elif h =='12':
            return
        else:
            return Response("No such horizon")
         
    elif  model == 'MLP':
        #fetch from bdd
        if h == '1':
            sales = ForecastedSales.objects.filter(product=pk,model_name=model)
            serializer = SalesForecastedSerializer(sales,many=True)
            return Response(serializer.data)
            
        elif h == '6':
            return
        elif h == '12':
            return
        else:
            return Response("No such horizon")
        return 
    elif  model == 'LSTM':
        #fetch from bdd
        if h == '1':
            sales = ForecastedSales.objects.filter(product=pk,model_name=model)
            serializer = SalesForecastedSerializer(sales,many=True)
            return Response(serializer.data)
            
        elif h == '6':
            return
        elif h == '12':
            return
        else:
            return Response("No such horizon")
        return
    else:
        return Response("No such model")
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#########################predictions###############################
#demanding to forecaste new values without retraining model
#this version uses the latest actual sale to give a new prediction
#needs to be updated to use a given starting date
@api_view(['GET'])
def Forecasting(request,pk,model,h):
    #1--get product instance
    product_instance = Product.objects.get(id=pk)
    #-2 create new date instance T+1 from latest T, for the 3 models forecasting
    previous_4_ordered_sales= ActualSales.objects.all().order_by('-date__date')[:4].values('quantity','date__date')      
    latest_date = previous_4_ordered_sales.values('date__date')[0].get('date__date')
    date_instance = Date.objects.create(date =latest_date)
    #3-call latest trained model

    #4- predict
    if model == "RF": #validated
        #call latest trained_model from bdd
        path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\RF_model.pkl" 
        trained_model=joblib.load(path)
        serilized_predictions = RF_predictions(product_instance,date_instance,trained_model,h)
        return Response(serilized_predictions)
    elif model == "MLP": #validated
        path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\MLP_model.h5" 
        trained_model = load_model(path)
        serilized_predictions = MLP_predictions(product_instance,date_instance,trained_model,h)
        return Response(serilized_predictions)
    elif model == "LSTM":
           #loading model & scaler!!path to change
        path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\LSTM_model.h5" 
        scaler_path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\lstm_scaler.pkl" 
        scaler = joblib.load(scaler_path)
        trained_model = load_model(path)
        #bring scaler of latest model
        scaler=""
        serilized_predictions = LSTM_predictions(product_instance,date_instance,trained_model,scaler,h)
        return Response(serilized_predictions)
    elif model == "auto":
        return
    else:
        return

#Training using all sales and forecasting new values
#(better when have new sales)
"validated"
@api_view(['GET'])
def Model_Training(request, pk,model,h):
#date option should be next month from laest actual month
    #1--get product instance
    product_instance = Product.objects.get(id=pk)
    #-2 create new date instance T+1 from latest T, for the 3 models forecasting
    previous_4_ordered_sales= ActualSales.objects.all().order_by('-date__date')[:4].values('quantity','date__date')      
    latest_date = previous_4_ordered_sales.values('date__date')[0].get('date__date')
    #date = date =datetime.date(2017, 1, 1) 
    #new_date = add_months(date,1)
    date_instance = Date.objects.create(date =latest_date)
    #3-choose model to train
    if model == 'RF': 
        #Training the model
        RF_trained_model, mape = RF_Training(pk,h)#instead of pickling
        #Predict using the model
        predictions = RF_predictions(product_instance,date_instance,RF_trained_model,h)
        #save them in forecastsales table

        #serialize them to send back

        return Response(predictions)
    elif  model == 'MLP':
        MLP_trained_model, mape = MLP_Training(pk,h)#instead of pickling
        #fetch from bdd
        predictions = MLP_predictions(product_instance,date_instance,MLP_trained_model,h)
        return Response(predictions)
    elif  model == 'LSTM':
        model_trained,scaler, mape = LSTM_Training(pk,h)#instead of pickling
        predictions = LSTM_predictions(product_instance,date_instance,model_trained,scaler,h)
        return Response(predictions)
    elif model == 'Best_model':
        #call 3 functions and compare their errors
        return 
    else:
        return Response("No such model")


#
#tests of serializer
#save it in bdd
#date_serializer = DateSerializer(date_instance)
#serializer= SalesForecastedSerializer(product=product_serializer, date=date_serializer,quantity= unistep )
#print(serializer)
#add to ForecastSales Model
#serializer.save()
###################"""save prediction end"##################

 
