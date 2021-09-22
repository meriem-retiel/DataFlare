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
import datetime 
import calendar

@api_view(['GET'])
def Prediction_Visualization(request,pk,model,h):
    print("in vizual")
    if model == 'RF':
        print("in RF") 
        if h == '1':
            print("in RF h1")
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
################################predictions#######################################

@api_view(['GET'])
def Model_Training(request, pk,model,h):
#date option should be next month from laest actual month
#then h horizon will define how many months we will give them
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
        predictions = RF_predictions(product_instance,date_instance,model,h)
        #save them in forecastsales table
        #serialize them to send back
        return Response(predictions)
    elif  model == 'MLP':
        #fetch from bdd
        predictions = MLP_predictions(product_instance,date_instance,model,h)
        return Response(predictions)
    elif  model == 'LSTM':
        predictions = LSTM_predictions(product_instance,date_instance,model,h)
        return Response(predictions)
    elif model == 'Best_model':
        #call 3 functions and compare their errors
        return 
    else:
        return Response("No such model")

def RF_predictions(product_instance,date_instance,model,horizon):
#fix paths later
    """short term prediction"""
    path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\RF_model.pkl" 
    #load the model
    RF=joblib.load(path)
    #extract last actual predictions after ordering by date__date
    previous_4_ordered_sales= ActualSales.objects.all().order_by('-date__date')[:4].values('quantity','date__date')      
    # convert quesryset to list => [t-1,t-2,t-3,t-4]
    list_result = [x.get('quantity') for x in previous_4_ordered_sales]
    #reverse list => [t-4,t-3,t-2,t-1]
    sales = [x for x in reversed(list_result)]
    #reshape list 1D to 2D
    sales_2D = np.reshape(sales, (1,4))
    #predict Quantity test[[ 6405. , 6303., 10953 , 6600]]=>14846 
    if horizon == '1' :
        unistep = RF.predict(sales_2D)
        forecast_instance= ForecastedSales.objects.get_or_create(quantity = unistep[0], product= product_instance, date = date_instance, model_name = model,horizon=horizon)
        #forecast_unistep.save()
        return unistep
    ###################"save prediction start##################
    #product_serializer = ProductSerializer(product_instance)
    elif horizon == '6':
        """Medium term prediction"""
        h_predictions = []
        for k in range(6):
            yhat = RF.predict(sales_2D)
            h_predictions = np.append(h_predictions,yhat)
            X = np.append(sales_2D[0][-3:], int(yhat))
            #reshape X 
            sales_2D = np.reshape(X, (1,4))
            #save instance
            previous_date = date_instance.date 
            new_date = add_months(previous_date,1)
            date_instance = Date.objects.create(date =new_date)
            forecast_instance= ForecastedSales.objects.get_or_create(quantity = yhat, product= product_instance, date = date_instance, model_name = model,horizon=horizon)

        return h_predictions 
        """long term prediction"""
    elif horizon == '12':
        h_predictions = []
        for k in range(12):
            yhat = RF.predict(sales_2D)
            h_predictions = np.append(h_predictions,yhat)
            X = np.append(sales_2D[0][-3:], int(yhat))
            #reshape X 
            sales_2D = np.reshape(X, (1,4))
            #save instance
            previous_date = date_instance.date 
            new_date = add_months(previous_date,1)
            date_instance = Date.objects.create(date =new_date)
            forecast_instance= ForecastedSales.objects.get_or_create(quantity = yhat, product= product_instance, date = date_instance, model_name = model,horizon=horizon)

        return h_predictions 
    else:
        return "No such model"
 #"array of all horizons [[t+1],[t-1,t-2,..,t-6],[t-1,....t+12]"

def MLP_predictions(product_instance,date_instance,model,horizon):
#fix paths later
    """short term prediction"""
    path = r"C:\Users\Yacine\PFE_dev_project\DataFlare\backend\src\products\MLapi\TrainedModels\MLP_model.h5" 
    MLP = load_model(path)
    #extract last actual predictions after ordering by date__date
    previous_4_ordered_sales= ActualSales.objects.all().order_by('-date__date')[:4].values('quantity','date__date')      
    # convert quesryset to list => [t-1,t-2,t-3,t-4]
    list_result = [x.get('quantity') for x in previous_4_ordered_sales]
    #reverse list => [t-4,t-3,t-2,t-1]
    sales = [x for x in reversed(list_result)]
    #reshape list 1D to 2D
    sales_3D = np.reshape(sales, (1, 1,4))#!recheck changed it to take only 4
    if horizon == '1' :
        unistep = MLP.predict(sales_3D,verbose=0)
        forecast_instance= ForecastedSales.objects.get_or_create(quantity = unistep[0][0][0], product= product_instance, date = date_instance, model_name = model,horizon=horizon)

        return unistep
    ###################"save prediction start##################
    #product_serializer = ProductSerializer(product_instance)
    elif horizon == '6':
        """Medium term prediction"""
        h_predictions = []
        for k in range(6):
            yhat = MLP.predict(sales_3D,verbose=0)
            h_predictions = np.append(h_predictions,yhat)
            X = np.append(sales_3D[0][0][-3:], int(yhat))
            #reshape X 
            sales_3D = np.reshape(X, (1, 1,4))#!recheck changed it to take only 4
            #save instance
            previous_date = date_instance.date 
            new_date = add_months(previous_date,1)
            date_instance = Date.objects.create(date =new_date)
            forecast_instance= ForecastedSales.objects.get_or_create(quantity = yhat, product= product_instance, date = date_instance, model_name = model,horizon=horizon)

        return h_predictions 
        """long term prediction"""
    elif horizon == '12':
        h_predictions = []
        for k in range(12):
            yhat = MLP.predict(sales_3D,verbose=0)
            h_predictions = np.append(h_predictions,yhat)
            X = np.append(sales_3D[0][0][-3:], int(yhat))
            #reshape X 
            sales_3D = np.reshape(X, (1, 1,4))#!recheck changed it to take only 4
            #save instance
            previous_date = date_instance.date 
            new_date = add_months(previous_date,1)
            date_instance = Date.objects.create(date =new_date)
            forecast_instance= ForecastedSales.objects.get_or_create(quantity = yhat, product= product_instance, date = date_instance, model_name = model,horizon=horizon)

        return h_predictions 
    else:
        return "No such model"

def LSTM_predictions(product_instance,date_instance,model,horizon):
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
    #differencing =>gives [t-5,t-4,t-3,t-2,t-1]
    sales_diff = difference(sales,1)# [  403.,  2930.,  -102.,  4650., -4353.]
    #scaling 
    sales=np.array(sales_diff).reshape(-1, len(sales_diff))#FROM LIST TO ARRAY 2D
    #scaler expects 5 timestamps as input
    sales_scaled = scaler.transform(sales.reshape(sales.shape[0], sales.shape[1]))
    #Predicting new value using 4 latest timestamps
    X = sales_scaled[0, 1:]
    X_3D = X.reshape(1, len(X), 1)
    """short term prediction"""
    if horizon == '1':
        pred = LSTM.predict(X_3D, batch_size=1)
        #inverse scale
        pred = invert_scale(scaler, X, pred) 
        ## invert differenced using previous real value
        unistep_prediction = pred + list_result[0] 
        forecast_instance= ForecastedSales.objects.get_or_create(quantity = unistep_prediction, product= product_instance, date = date_instance, model_name = model,horizon=horizon)

        return  unistep_prediction
    elif horizon == '6':
        """Medium term prediction"""
        h_predictions = []
        for k in range(6):
            pred_scaled = LSTM.predict(X_3D, batch_size=1)
            #inverse scale
            pred = invert_scale(scaler, X, pred_scaled) 
            ## invert differenced using previous real value
            if k == 0:
                prediction = pred + list_result[0]#latest original value non diff
            else:
                prediction = pred + h_predictions[k-1] #latest pedicted value non diff
                
            h_predictions = np.append(h_predictions,prediction)
            X = np.append(X_3D[0][-3:], [int(pred_scaled)])
            #reshape X
            X_3D = X.reshape(1, len(X), 1)
            #save instance
            previous_date = date_instance.date 
            new_date = add_months(previous_date,1)
            date_instance = Date.objects.create(date =new_date)
            forecast_instance= ForecastedSales.objects.get_or_create(quantity = prediction, product= product_instance, date = date_instance, model_name = model,horizon=horizon)

        return h_predictions 
        """long term prediction"""
    elif horizon == '12':
        h_predictions = []
        for k in range(12):
            pred_scaled = LSTM.predict(X_3D, batch_size=1)
            #inverse scale
            pred = invert_scale(scaler, X, pred_scaled) 
            ## invert differenced using previous real value
            if k == 0:
                prediction = pred + list_result[0]#latest original value non diff
            else:
                prediction = pred + h_predictions[k-1] #latest pedicted value non diff
                
            h_predictions = np.append(h_predictions,prediction)
            X = np.append(X_3D[0][-3:], [int(pred_scaled)])
            #reshape X
            X_3D = X.reshape(1, len(X), 1)
            #save instance
            previous_date = date_instance.date 
            new_date = add_months(previous_date,1)
            date_instance = Date.objects.create(date =new_date)
            forecast_instance= ForecastedSales.objects.get_or_create(quantity = prediction, product= product_instance, date = date_instance, model_name = model,horizon=horizon)

        return h_predictions 
         
    else:
        return "No such model"    

#tests of serializer
#save it in bdd
#date_serializer = DateSerializer(date_instance)
#serializer= SalesForecastedSerializer(product=product_serializer, date=date_serializer,quantity= unistep )
#print(serializer)
#add to ForecastSales Model
#serializer.save()
###################"""save prediction end"##################

      
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

