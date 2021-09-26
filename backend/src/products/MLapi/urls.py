from django.urls import path, include
from .views import Prediction_Visualization,Forecasting, Model_Training

urlpatterns = [
    path('ForecastedSales/<pk>/<model>/<h>/',Prediction_Visualization),
    #path('Training/<pk>/<model>/<h>/',Model_Training),#Validated
    path('Predict/<pk>/<model>/<h>',Forecasting),
    #'Predict/<pk>/<model>/<h>/<date>'
]
