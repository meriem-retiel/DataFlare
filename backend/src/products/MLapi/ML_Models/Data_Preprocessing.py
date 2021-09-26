# forecast monthly with random forest
from pandas import DataFrame
from pandas import concat
from sklearn.metrics import mean_absolute_error
from matplotlib import pyplot
import pandas as pd
import numpy as np
import datetime 
import calendar
from math import sqrt
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import numpy
# transform a time series dataset into a supervised learning dataset
def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):   
    df = DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('t-%d' % (i))] 
        #names += [('x%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('t') ]
            #names += [('y%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('t+%d' % (i))]
            #names += [('y%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg
 
# split a univariate dataset into train/test sets
def train_test_split(data, n_test):
    return data.iloc[:-n_test, :], data.iloc[-n_test:, :]

def ANN_train_test_split(data, n_test):
	return data[:-n_test, :], data[-n_test:, :]

def evaluate_multistep(y_h_steps,predicted_h_steps):
    
    h_mae =  mean_absolute_error(y_h_steps, predicted_h_steps)
    h_rmse = sqrt(mean_squared_error(y_h_steps, predicted_h_steps))
    h_mape = mape(y_h_steps,predicted_h_steps) 
    return h_mae,h_rmse,h_mape

#error
def mape(actual, pred): 
    actual, pred = np.array(actual), np.array(pred)
    MAPE = np.mean(np.abs((actual - pred) / actual)) * 100
    #print('MAPE : %.1f' % MAPE)
    return MAPE

# create a differenced series
def difference(dataset, interval=1):
	diff = []
	for i in range(interval, len(dataset)):
		value = dataset[i] - dataset[i - interval]
		diff = np.append(diff, value) #diff.append(value)
	return diff

# invert differenced value
def inverse_difference(history, yhat, interval=1):
	return yhat + history[-interval]

# scale train and test data to [-1, 1]
def scale(train, test):
	# fit scaler
	scaler = MinMaxScaler(feature_range=(-1, 1))
	scaler = scaler.fit(train)
	# transform train
	train = train.reshape(train.shape[0], train.shape[1])
	train_scaled = scaler.transform(train)
	# transform test
	test = test.reshape(test.shape[0], test.shape[1])
	test_scaled = scaler.transform(test)
	return scaler, train_scaled, test_scaled

# inverse scaling for a forecasted value
def invert_scale(scaler, X, yhat):
	new_row = [x for x in X] + [yhat]
	array = numpy.array(new_row)#############gave some warning
	array = array.reshape(1, len(array))
	inverted = scaler.inverse_transform(array)
	return inverted[0, -1]

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)
