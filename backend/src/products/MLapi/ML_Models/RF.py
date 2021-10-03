#uses all salesactual to train
#takes in entry hyuperparams or uses default
#give back trained model usinf walk forward
#give back mpae error
from sklearn.ensemble import RandomForestRegressor
from numpy import asarray
import numpy as np
from math import sqrt
from sklearn.metrics import mean_squared_error
from ...api.serializers import SalesForecastedSerializer
from ...models import ActualSales,ForecastedSales,Date, ActualSales
from .Data_Preprocessing import add_months, mean_absolute_error,mape, series_to_supervised, train_test_split,evaluate_multistep
################"Mai-function"################

#create and save RF predictions
def RF_predictions(product_instance,date_instance,trained_model,horizon):
#fix paths later
    """short term prediction"""
    RF = trained_model
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
        previous_date = date_instance.date 
        new_date = add_months(previous_date,1)
        date_instance, create = Date.objects.get_or_create(date =new_date)
        forecast_instance , created = ForecastedSales.objects.get_or_create(quantity = unistep[0], product= product_instance, date = date_instance, model_name = 'RF',horizon=horizon)
        #Serilize forecaste
        #a = ForecastedSales.objects.filter(id_forcast = forecast_instance['id'])
        serializer = SalesForecastedSerializer(forecast_instance)
        #unistep_serialized = SalesForecastedSerializer(forecast_instance[0],many=True)
        #print("after serilaizing")
        return serializer 
    ###################"save prediction start##################
    #product_serializer = ProductSerializer(product_instance)
    elif horizon == '6':
        """Medium term prediction"""
        h_predictions = []
        instances = []
        for k in range(6):
            yhat = RF.predict(sales_2D)
            h_predictions = np.append(h_predictions,int(yhat))
            X = np.append(sales_2D[0][-3:], int(yhat))
            #reshape X 
            sales_2D = np.reshape(X, (1,4))
            #save instance
            previous_date = date_instance.date 
            new_date = add_months(previous_date,1)
            date_instance, create = Date.objects.get_or_create(date =new_date)
            forecast_instance, create= ForecastedSales.objects.get_or_create(quantity = int(yhat), product= product_instance, date = date_instance, model_name = 'RF',horizon=horizon)
            instances = np.append(instances,forecast_instance )
      
        serializer = SalesForecastedSerializer(instances,many=True)
            #forecast_instance= ForecastedSales.objects.get_or_create(quantity = yhat, product= product_instance, date = date_instance, model_name = model,horizon=horizon)

        return serializer 
        """long term prediction"""
    elif horizon == '12':
        h_predictions = []
        instances = []
        for k in range(12):
            yhat = RF.predict(sales_2D)
            h_predictions = np.append(h_predictions,yhat)
            X = np.append(sales_2D[0][-3:], int(yhat))
            #reshape X 
            sales_2D = np.reshape(X, (1,4))
            #save instance

            previous_date = date_instance.date 
            new_date = add_months(previous_date,1)
            date_instance, create = Date.objects.get_or_create(date =new_date)
            forecast_instance, create= ForecastedSales.objects.get_or_create(quantity = int(yhat), product= product_instance, date = date_instance, model_name = 'RF',horizon=horizon)
            instances = np.append(instances,forecast_instance )
        serializer = SalesForecastedSerializer(instances,many=True)

        return serializer 
    else:
        return "No such model"
 #"array of all horizons [[t+1],[t-1,t-2,..,t-6],[t-1,....t+12]"


#training model
def RF_Training(ProdID, horizon, hyperparam_array=None):
    window = 4
    param = 80 #from grid search later
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

    #launch training
    model = "trained model depending on horizon"
    data_supervised = series_to_supervised(sales,window)
    print(data_supervised)

    if horizon == '1':
         rmse_metric, mape_metric, mae_metric, y, yhat, RF_model = RF_unistep_walk_forward_validation(data_supervised, test_size,param)
         return RF_model,mape_metric
    elif horizon == '6':
         rmse_metric, mape_metric, mae_metric, test, RF_model = RF_mediumterm_walk_forward_validation(data_supervised, test_size,param)
         return RF_model,mape_metric
    elif horizon == '12':
         print()
         rmse_metric, mape_metric, mae_metric, test, RF_model = RF_longterm_walk_forward_validation(data_supervised, test_size,param)
         return RF_model,mape_metric
    else:
        return "no such horizon"
 
################"Sub-function"################
    # fit an random forest model and make a one step prediction
def random_forest_forecast(train, testX,n_estimators):
    # transform list into array**************train is not a list tho !!!!!
    print('inside random' )
    train = asarray(train)
    # split into input and output columns
    trainX, trainy = train[:, :-1], train[:, -1]
    # fit model
    #model = RandomForestRegressor(n_estimators)
    model = RandomForestRegressor()#?whats point of walk_forwrd if last model we get used is one who was trained by whole data
    model.fit(trainX, trainy)
    #	print("model.score")
    #	print(model.score)
    #print(model.get_params())
    # make a one-step prediction
    yhat = model.predict([testX])
    #convert to integer in python
    return yhat[0], model
######backtest ML models in time series
"validated"
# walk-forward validation for univariate data
def RF_unistep_walk_forward_validation(data, n_test,n_estimators):
    predictions = list()
    # split dataset
    train, test = train_test_split(data, n_test)
    # seed history with training datase
    history = train #history = [x for x in train]
    # step over each time-step in the test set
    for i in range(len(test)):
        # split test row into input and output columns
        testX, testy = test.iloc[i, :-1], test.iloc[i, -1]        
        # fit model on history and make a prediction
        yhat, model = random_forest_forecast(history, testX,n_estimators) #yhat = random_forest_forecast(history, testX)
        # store forecast in list of predictions
        predictions.append(yhat)
        # add actual observation to history for the next loop
        history = history.append(test.iloc[i]) #===> need it to use in next iteration
        # summarize progress
    #print('> Month=%d, expected=%.1f, predicted=%.1f' % (i+1,testy, yhat))
    # estimate prediction error
    mae = mean_absolute_error(test.iloc[:, -1], predictions)
    rmse = sqrt(mean_squared_error(test.iloc[:, -1], predictions))
    mape_error= mape(test.iloc[:, -1],predictions)
    return rmse, mape_error, mae, test.iloc[:, -1], predictions, model


#for one product
"validated"
def RF_mediumterm_walk_forward_validation(supervised_data, test_size,n_estimators):
    mae = list()
    rmse = list()
    mape = list()
    h_predictions = list()
    test_h_y = []
    
    # split dataset
    train, test = train_test_split(supervised_data,test_size)
    loop_size = len(test) - 6 #must test size>16
    print(loop_size)
    print(loop_size)
    # seed history with training datase
    history = train
    # step over each time-step in the test set
    for i in range(loop_size):#change this 3 for future data size
         # cuz we can form only 3 h_y of 6 months to test 
        # split test row into input and output columns
        testX= test.iloc[i, :-1] 
        test_h_y = []
        h_predictions = list()
        for x in range(i,i+6):#!!!!
            #test_h_y.append(test.iloc[x,-1])
            test_h_y =  np.append(test_h_y, test.iloc[x,-1])#to form y=[t+1, t+2,....,t+6]
        # fit model on history and make a prediction
        #1st month
        for k in range(6):
            yhat, model = random_forest_forecast(history, testX,n_estimators) 
            h_predictions.append(yhat)
            testX = np.append(testX[-3:], int(yhat))      
        h_mae,h_rmse,h_mape = evaluate_multistep(test_h_y, h_predictions)
        history.append(test.iloc[i])
        #np.append(history,test[i] )
        mae.append(h_mae)
        rmse.append(h_rmse)
        mape.append(h_mape) 
    h_mape= np.mean(np.array(mape))
    h_mae =  np.mean(np.array(mae))
    h_rmse = np.mean(np.array(rmse))
    #average of each metric
    return h_rmse,h_mape, h_mae, test, model 

"validated"
def RF_longterm_walk_forward_validation(supervised_data, test_size,n_estimators):
    mae = list()
    rmse = list()
    mape = list()
    h_predictions = list()
    test_h_y = []
    
    # split dataset
    train, test = train_test_split(supervised_data,test_size)
    loop_size = len(test) -12 #must test size>16
    # seed history with training datase
    history = train
    # step over each time-step in the test set
    for i in range(loop_size): # cuz we can form only 3 h_y of 6 months to test 
        # split test row into input and output columns
        testX= test.iloc[i, :-1] 
        test_h_y = []
        h_predictions = list()
        print("inside wfv before loop of 12")                 

        for x in range(i,i+12):#!!!!
            test_h_y =  np.append(test_h_y, test.iloc[x,-1])#to form y=[t+1, t+2,....,t+6]
        print("inside wfv of 12")                 

        yhat, model = random_forest_forecast(history, testX,n_estimators) 
        h_predictions.append(yhat)
        testX = np.append(testX[-3:], int(yhat))
        for k in range(11):
            yhat = model.predict([testX])
            h_predictions.append(yhat)
            testX = np.append(testX[-3:], int(yhat)) 
                
        h_mae,h_rmse,h_mape = evaluate_multistep(test_h_y, h_predictions)
        history.append(test.iloc[i])
        mae.append(h_mae)
        rmse.append(h_rmse)
        mape.append(h_mape)
    h_mape= np.mean(np.array(mape))
    h_mae =  np.mean(np.array(mae))
    h_rmse = np.mean(np.array(rmse))
    return h_mae,h_rmse,h_mape, test, model
