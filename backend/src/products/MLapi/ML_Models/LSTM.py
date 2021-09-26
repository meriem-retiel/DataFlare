from sklearn.metrics import mean_squared_error
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from math import sqrt
from math import sqrt
#from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import pandas as pd
import numpy as np
from numpy import concatenate
import statistics

from ...models import ActualSales,ForecastedSales,Date, ActualSales
from .Data_Preprocessing import add_months, series_to_supervised, mape, series_to_supervised,ANN_train_test_split, difference,inverse_difference,scale,invert_scale, evaluate_multistep

#trainging the model
def LSTM_Training(ProdID,horizon):
    window = 4
    epochs = 100
    batch_size=80
    test_size = 16
    sales = ActualSales.objects.filter(product_id = ProdID).order_by('-date__date').values('quantity','date__date')
    #test_size = int(len(sales)*0.3)#30% test
    # convert quesryset to list => [t-10....t-4,t-3,t-2,t-1] 
    list_sales = [x.get('quantity') for x in sales]
    # reverse list => [t-1,t-2,t-3,t-4....]
    sales = [x for x in reversed(list_sales)]
    print(sales)
    print("sales for lstm")
    #data_supervised = series_to_supervised(sales,window)   
    #print(data_supervised)
    #data_supervised = data_supervised.values
    if horizon == '1': #took around 
        mae_metric, rmse_metric, mape_metric, model,scaler = LSTM_unistep_WFV(sales,window,test_size)
        return model, scaler,mape_metric
    elif horizon == "6":
        mae_metric, rmse_metric, mape_metric, model,scaler = LSTM_mediumterm_WFV(sales,window,test_size)
        return model,scaler,mape_metric
    elif horizon == "12":
        mae_metric, rmse_metric, mape_metric, model,scaler = LSTM_longterm_WFV(sales,window,test_size)
        return model,scaler, mape_metric
    else:
        return "no such horizon"
# fit an LSTM network to training data
def fit_lstm(train, batch_size, nb_epoch, neurons, timesteps):
	X, y = train[:, 0:-1], train[:, -1]
	X = X.reshape(X.shape[0], timesteps, 1)
	model = Sequential()
	model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=True))
	model.add(Dense(1))
	model.compile(loss='mean_squared_error', optimizer='adam')
	for i in range(nb_epoch):
		model.fit(X, y, epochs=1, batch_size=batch_size, verbose=0, shuffle=False)
		model.reset_states()
	return model

#create and save LSTM predictions
def LSTM_predictions(product_instance,date_instance,model_trained,scaler,horizon):
    LSTM = model_trained
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
        forecast_instance= ForecastedSales.objects.get_or_create(quantity = unistep_prediction, product= product_instance, date = date_instance, model_name = "LSTM",horizon=horizon)

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
            forecast_instance= ForecastedSales.objects.get_or_create(quantity = prediction, product= product_instance, date = date_instance, model_name = "LSTM",horizon=horizon)

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
            forecast_instance= ForecastedSales.objects.get_or_create(quantity = prediction, product= product_instance, date = date_instance, model_name = "LSTM",horizon=horizon)

        return h_predictions 
         
    else:
        return "No such model"    



# make a one-step forecast
def forecast_lstm(model, batch_size, X):
	X = X.reshape(1, len(X), 1)
	yhat = model.predict(X, batch_size=batch_size)
	return yhat[0,0]
"validated"
def LSTM_unistep_WFV(raw_values, timesteps,test_size):
    print("inside wfv lstm")
    # transform data to be stationary
    diff_values = difference(raw_values, 1)
    # transform data to be supervised learning
    supervised  = series_to_supervised(diff_values,timesteps) 
    supervised_values = supervised.values
    # split data into train and test-sets
    train, test = ANN_train_test_split(supervised_values,test_size)
    # transform the scale of the data
    scaler, train_scaled, test_scaled = scale(train, test)
    history = train_scaled
    # forecast test dataset
    predictions = list()
    for i in range(len(test_scaled)):
        # predict
        X, y = test_scaled[i, 0:-1], test_scaled[i, -1]
        lstm_model = fit_lstm(history, 1, 500, 1, timesteps)#fit
        yhat = forecast_lstm(lstm_model, 1, X)#test
        # invert scaling
        yhat = invert_scale(scaler, X, yhat)
        # invert differencing
        yhat = inverse_difference(raw_values, yhat, len(test_scaled)+1-i)
        # store forecast
        predictions.append(yhat)
        np.append(history, test_scaled[i])
    # report performance
    mae = mean_absolute_error(raw_values[-test_size:], predictions)
    rmse = sqrt(mean_squared_error(raw_values[-test_size:], predictions))
    mape_error = mape(raw_values[-test_size:], predictions)
    return mae, mape_error,rmse,lstm_model,scaler
"validated"
def LSTM_mediumterm_WFV(raw_values, timesteps,test_size):
    # transform data to be stationary
    diff_values = difference(raw_values, 1)
    # transform data to be supervised learning
    supervised  = series_to_supervised(diff_values,timesteps) 
    supervised_values = supervised.values
    # split data into train and test-sets
    train, test = ANN_train_test_split(supervised_values,test_size)
    # transform the scale of the data
    scaler, train_scaled, test_scaled = scale(train, test)
    history = train_scaled 
    test_h_y = []   
    loop_size = len(test_scaled)- 6
    #print(loop_size)###10
    for i in range(loop_size): # cuz we can form only 3 h_y of 6 months to test 
        testX= test_scaled[i, :-1]
        test_h_y = []
        predict_h_y = list()
        h_predictions = list()
        mae = list()
        rmse = list()
        mape = list()
        for x in range(i,i+6):#!!!!outta range
            test_h_y =  np.append(test_h_y, test_scaled[x,-1])#to form [t+1, t+2,....,t+6]
        lstm_model = fit_lstm(history, 1, 500, 1, timesteps)
        for k in range(6):
            yhat = forecast_lstm(lstm_model, 1, testX)
            predict_h_y.append(yhat)#not inversed
            yhat = invert_scale(scaler, testX, yhat)#!!!!
            print(len(supervised_values)+1-i-k)
            yhat = inverse_difference(raw_values, yhat, len(supervised_values)+1-i-k) 
            h_predictions.append(yhat)#inversed    
            testX = np.append(testX[-3:], int(yhat))
        h_mae,h_rmse,h_mape = evaluate_multistep(test_h_y, predict_h_y)#both inversed
        np.append(history, test_scaled[i])#WFV
        mae.append(h_mae)
        rmse.append(h_rmse)
        mape.append(h_mape)
    h_mape =  statistics.mean(mape) 
    h_mae = statistics.mean(mae) 
    h_rmse = statistics. mean(rmse)
    return h_mae, h_mape,h_rmse ,lstm_model,scaler
"validated"
def LSTM_longterm_WFV(raw_values, timesteps,test_size):
    # transform data to be stationary
    diff_values = difference(raw_values, 1)
    # transform data to be supervised learning
    supervised  = series_to_supervised(diff_values,timesteps) 
    supervised_values = supervised.values
    # split data into train and test-sets
    train, test = ANN_train_test_split(supervised_values,test_size)
    # transform the scale of the data
    scaler, train_scaled, test_scaled = scale(train, test)
    history = train_scaled 
    test_h_y = []   
    loop_size = len(test_scaled)- 12
    #print(loop_size)###10
    for i in range(loop_size): # cuz we can form only 3 h_y of 6 months to test 
        testX= test_scaled[i, :-1]
        test_h_y = []
        predict_h_y = list()
        h_predictions = list()
        mae = list()
        rmse = list()
        mape = list()
        for x in range(i,i+12):#!!!!outta range
            test_h_y =  np.append(test_h_y, test_scaled[x,-1])#to form [t+1, t+2,....,t+6]
        lstm_model = fit_lstm(history, 1, 500, 1, timesteps)
        for k in range(12):
            yhat = forecast_lstm(lstm_model, 1, testX)
            predict_h_y.append(yhat)#not inversed
            yhat = invert_scale(scaler, testX, yhat)#!!!!
            yhat = inverse_difference(raw_values, yhat, len(supervised_values)+1-i-k) 
            h_predictions.append(yhat)#inversed    
            testX = np.append(testX[-3:], int(yhat))
        h_mae,h_rmse,h_mape = evaluate_multistep(test_h_y, predict_h_y)#both inversed
        np.append(history, test_scaled[i])#WFV
        mae.append(h_mae)
        rmse.append(h_rmse)
        mape.append(h_mape)
    h_mape =  statistics.mean(mape) 
    h_mae = statistics.mean(mae) 
    h_rmse = statistics. mean(rmse)
    return h_mae, h_mape,h_rmse ,lstm_model,scaler