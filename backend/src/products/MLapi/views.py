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

from .ML_Models.Data_Preprocessing import add_months
from .ML_Models.RF import RF_Training, RF_predictions
from .ML_Models.MLP import MLP_Training, MLP_predictions
from .ML_Models.LSTM import LSTM_Training, LSTM_predictions

#validated
@api_view(['GET'])
def Prediction_Visualization(request,pk,model,h):
    if model in ('RF', 'MLP','LSTM'):
        if h in ('1', '6', '12'):
            sales = ForecastedSales.objects.filter(product=pk,model_name=model, horizon = h)
            serializer = SalesForecastedSerializer(sales,many=True)
            print(sales)
            print("here slaes was serilized normally")
            return Response(serializer.data)  
        else:
            return Response("No such horizon")
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
    product_instance = Product.objects.get(id_prod=pk)
    #-2 create new date instance T+1 from latest T, for the 3 models forecasting
    previous_4_ordered_sales= ActualSales.objects.all().order_by('-date__date')[:4].values('quantity','date__date')      
    latest_date = previous_4_ordered_sales.values('date__date')[0].get('date__date')
    date_instance , created = Date.objects.get_or_create(date =latest_date)
    #3-call latest trained model

    #4- predict
    if model == "RF": #validated
        #call latest trained_model from bdd or files***********************
        path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\RF_model.pkl" 
        trained_model=joblib.load(path)
        serializer = RF_predictions(product_instance,date_instance,trained_model,h)
        return Response(serializer.data)
    elif model == "MLP": #validated
        #call latest trained_model from bdd***********************
        path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\MLP_model.h5" 
        trained_model = load_model(path)
        serializer = MLP_predictions(product_instance,date_instance,trained_model,h)
        ######################################""
        print("before response serilized")
        print(serializer)
        return Response(serializer.data)
    elif model == "LSTM":
        #call latest trained_model from bdd***********************
        #loading model & scaler!!path to change
        path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\LSTM_model.h5" 
        scaler_path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\lstm_scaler.pkl" 
        
        scaler = joblib.load(scaler_path)
        trained_model = load_model(path)
        serializer = LSTM_predictions(product_instance,date_instance,trained_model,scaler,h)
        return Response(serializer.data)
    elif model == "auto":
        return
    else:
        return "No such model"

#Training using all sales and forecasting new values
#(better when have new sales)
"validated"
@api_view(['GET'])
def Model_Training(request, pk,model,h):
#date option should be next month from laest actual month
    #1--get product instance
    product_instance = Product.objects.get(id_prod=pk)
    #-2 create new date instance T+1 from latest T, for the 3 models forecasting
    previous_4_ordered_sales= ActualSales.objects.all().order_by('-date__date')[:4].values('quantity','date__date')      
    latest_date = previous_4_ordered_sales.values('date__date')[0].get('date__date')
    
    date_instance, created = Date.objects.get_or_create(date =latest_date)
    #3-choose model to train
    if model == 'RF': 
        #Training the model
        RF_trained_model, mape = RF_Training(pk,h)#instead of pickling
        #Predict using the model & are saved in BDD
        predictions = RF_predictions(product_instance,date_instance,RF_trained_model,h)
        #serialize them to send back
        #serializer of "mape" & "object of predictions"
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

 
