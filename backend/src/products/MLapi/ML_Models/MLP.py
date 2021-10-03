from math import sqrt
from ...api.serializers import SalesForecastedSerializer

from pandas.core.frame import DataFrame
#from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import MinMaxScaler
import statistics
import numpy as np
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Dense
from ...models import ActualSales,ForecastedSales,Date, ActualSales
from .Data_Preprocessing import add_months,series_to_supervised, mape, ANN_train_test_split, series_to_supervised, evaluate_multistep

#create and save MLP predictions
def MLP_predictions(product_instance,date_instance,model_trained,horizon):
#fix paths later
    """short term prediction"""
    
    MLP= model_trained
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
        #save instance
        previous_date = date_instance.date 
        new_date = add_months(previous_date,1)
        date_instance, create = Date.objects.get_or_create(date =new_date)
        forecast_instance , created = ForecastedSales.objects.get_or_create(quantity = int(unistep[0]), product= product_instance, date = date_instance, model_name = 'MLP',horizon=horizon)
        serializer = SalesForecastedSerializer(forecast_instance)

        return serializer
    ###################"save prediction start##################
    #product_serializer = ProductSerializer(product_instance)
    elif horizon == '6':
        """Medium term prediction"""
        h_predictions = []
        instances = []
        for k in range(6):
            yhat = MLP.predict(sales_3D,verbose=0)
            h_predictions = np.append(h_predictions,yhat)
            X = np.append(sales_3D[0][0][-3:], int(yhat))
            #reshape X 
            sales_3D = np.reshape(X, (1, 1,4))#!recheck changed it to take only 4
            #save instance
            previous_date = date_instance.date 
            new_date = add_months(previous_date,1)
            date_instance, create = Date.objects.get_or_create(date =new_date)
            forecast_instance , created = ForecastedSales.objects.get_or_create(quantity = int(yhat), product= product_instance, date = date_instance, model_name = 'MLP',horizon=horizon)
            instances = np.append(instances,forecast_instance )
        serializer = SalesForecastedSerializer(instances,many=True)

        return serializer 
        """long term prediction"""
    elif horizon == '12':
        h_predictions = []
        instances = []
        for k in range(12):
            yhat = MLP.predict(sales_3D,verbose=0)
            h_predictions = np.append(h_predictions,yhat)
            X = np.append(sales_3D[0][0][-3:], int(yhat))
            #reshape X 
            sales_3D = np.reshape(X, (1, 1,4))#!recheck changed it to take only 4
            #save instance
            previous_date = date_instance.date 
            new_date = add_months(previous_date,1)
            date_instance, create = Date.objects.get_or_create(date =new_date)
            forecast_instance , created = ForecastedSales.objects.get_or_create(quantity = int(yhat), product= product_instance, date = date_instance, model_name = 'MLP',horizon=horizon)
            instances = np.append(instances,forecast_instance )
        serializer = SalesForecastedSerializer(instances,many=True)

        return serializer 
    else:
        return "No such model"



#training model
def MLP_Training(ProdID, horizon, hyperparam_array=None):
    window = 4
    epochs = 100
    batch_size=80
    test_size = 16 # ( min need 16 to do 12 prediction)
    #if hyperparam_array==None 
        # then call gridsearch
    # fitch ordered sales by date and get quantity only
    #[{t-10}.....{t-1 3475 2018},{t 3072 2017}]
    sales = ActualSales.objects.filter(product_id = ProdID).order_by('-date__date').values('quantity','date__date')
    #test_size = int(len(sales)*0.3)#30% test
    # convert quesryset to list => [t-10....t-4,t-3,t-2,t-1] 
    list_sales = [x.get('quantity') for x in sales]
    # reverse list => [t-1,t-2,t-3,t-4....]
    sales = [x for x in reversed(list_sales)]
    print(sales)
    print("sales for mlp")
    #launch training
    model = "trained model depending on horizon"
    data_supervised = series_to_supervised(sales,window)   
    print(data_supervised)
    data_supervised = data_supervised.values
    print(data_supervised)
    if horizon == '1': #took around 8 sec
         mae_metric, rmse_metric, mape_metric, model = MLP_unistep_walk_forward_validation(data_supervised,test_size, batch_size,epochs)
         return model,mape_metric
    elif horizon == '6': #10sec
         mae_metric, rmse_metric, mape_metric, model = MPL_mediumterm_walk_forward_validation(data_supervised,test_size, batch_size,epochs)
         return model,mape_metric
    elif horizon == '12': #10 sec
         mae_metric, rmse_metric, mape_metric, model=  MLP_longterm_walk_forward_validation(data_supervised,test_size, batch_size,epochs)
         return model, mape_metric 
    else:
        return "no such horizon"
     
def fit_mlp(train,batch_size,epochs):
    X, y = train[:, 0:-1], train[:, -1]
    print('after added iloc in fit_mlp')
    
    window = X.shape[1]#!!!!
    #np.reshape(X,) 
    X = X.reshape(X.shape[0], 1, X.shape[1])
    model = Sequential()
    model.add(Dense(50, activation='relu', input_dim=window))
    model.add(Dense(1))
    #	model.compile(optimizer='adam', loss='mse',metrics=['accuracy'])
    model.compile(optimizer='adam', loss='mse',metrics=[keras.metrics.MeanAbsolutePercentageError()])
    model.fit(X, y, batch_size= batch_size, epochs = epochs, verbose=0)
    scores = model.evaluate(X, y, verbose=0)
    #print("%.3f" % ( scores))
    evaluation = model.evaluate(X, y)
    return model, evaluation

# make a one-step forecast
def forecast_mlp(model, X):
    X = X.reshape(1, 1, len(X))
    yhat = model.predict(X,verbose=0)
    return yhat[0,0]
"validated"
def MLP_unistep_walk_forward_validation(supervised_data, test_size,batch_size,epochs):
    predictions = list()
    # split dataset
    train, test = ANN_train_test_split(supervised_data,test_size)
    # seed history with training datase
    ###################!!!!!!!!!!!!!!here prob
    history = train
    # step over each time-step in the test set
    for i in range(len(test)):
        # split test row into input and output columns
        testX, testy = test[i, :-1], test[i, -1]        
        # fit model on history and make a prediction
        model, model_evaluation = fit_mlp(history,batch_size,epochs)
        yhat = forecast_mlp(model, testX) #yhat = random_forest_forecast(history, testX)
        # store forecast in list of predictions
        predictions.append(yhat)
        # add actual observation to history for the next loop
        #history.append(test.iloc[i]) #===> need it to use in next iteration
        np.append(history, test[i])
    # estimate prediction error
    mae = mean_absolute_error(test[:, -1], predictions)
    rmse = sqrt(mean_squared_error(test[:, -1], predictions))
    mape_error= mape(test[:, -1],predictions) 
    #print('MAPE: %.3f for n_estimators: %d ' % (mape_error, n_estimators))
    return mae,rmse,mape_error, model
"validated"
def MPL_mediumterm_walk_forward_validation(supervised_data, test_size,batch_size,epochs):
    mae = list()
    rmse = list()
    mape = list()
    h_predictions = list()
    # split dataset
    train, test = ANN_train_test_split(supervised_data,test_size)
    # seed history with training datase
    history = train
    loop_size = len(test) - 6 #must test size>16
    # step over each time-step in the test set
    for i in range(loop_size): # cuz we can form only 3 h_y of 6 months to test 
        # split test row into input and output columns
        testX= test[i, :-1]
        test_h_y = []
        h_predictions = list()
        for x in range(i,i+6):#!!!!
            test_h_y =  np.append(test_h_y, test[x,-1])#to form [t+1, t+2,....,t+6]
        print(i)
        print('test_h_y')
        print(test_h_y)

        # fit model on history and make a prediction
        model, model_evaluation = fit_mlp(history,batch_size,epochs)
        ##################"do a loop bookle later"
        # to stop before reaching last sample         
        #1st month
        for j in range(6):
            yhat = forecast_mlp(model, testX)
            h_predictions.append(yhat)
            testX = np.append(testX[-3:], int(yhat))
        h_mae,h_rmse,h_mape = evaluate_multistep(test_h_y, h_predictions)
        np.append(history, test[i])
        mae.append(h_mae)
        rmse.append(h_rmse)
        mape.append(h_mape)
    h_mape =  statistics.mean(mape) 
    h_mae = statistics.mean(mae) 
    h_rmse = statistics. mean(rmse) 

    return h_mae,h_rmse,h_mape, model
"validated"
def MLP_longterm_walk_forward_validation(supervised_data, test_size,batch_size,epochs):
    mae = list()
    rmse = list()
    mape = list()
    h_predictions = list()
    # split dataset
    train, test = ANN_train_test_split(supervised_data,test_size)
    # seed history with training datase
    history = train
    loop_size = len(test) - 12 #must test size>16
    # step over each time-step in the test set
    for i in range(loop_size): # cuz we can form only 3 h_y of 6 months to test 
        # split test row into input and output columns
        testX= test[i, :-1]
        test_h_y = []
        h_predictions = list()
        for x in range(i,i+12):
            test_h_y =  np.append(test_h_y, test[x,-1])#to form [t+1, t+2,....,t+6]
        print(i)
        print('test_h_y')
        print(test_h_y)
        # fit model on history and make a prediction
        model, model_evaluation = fit_mlp(history,batch_size,epochs)        
        for k in range(12):
            yhat = forecast_mlp(model, testX)
            h_predictions.append(yhat)
            testX = np.append(testX[-3:], int(yhat))
               
        h_mae,h_rmse,h_mape = evaluate_multistep(test_h_y, h_predictions)
        np.append(history, test[i])
        mae.append(h_mae)
        rmse.append(h_rmse)
        mape.append(h_mape)
    h_mape =  statistics.mean(mape) 
    h_mae = statistics.mean(mae) 
    h_rmse = statistics. mean(rmse) 
    return h_mae,h_rmse,h_mape, model