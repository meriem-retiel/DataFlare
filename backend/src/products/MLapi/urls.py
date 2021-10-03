from django.urls import path, include
from .views import Prediction_Visualization,Forecasting, Model_Training

urlpatterns = [
    #validated
    path('ForecastedSales/<pk>/<model>/<h>/',Prediction_Visualization),
    #validated
    path('Training/<pk>/<model>/<h>/',Model_Training),#Validated
    #validated
    path('Predict/<pk>/<model>/<h>/',Forecasting),
    #'Predict/<pk>/<model>/<h>/<date>'
]
