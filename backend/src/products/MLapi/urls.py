from django.urls import path, include
from .views import Prediction_Visualization, Model_Training

urlpatterns = [
   # path('<pk>/<model>/<h>/',Prediction_Visualization),#get request
    path('train/<pk>/<model>/<h>/',Model_Training),#get request

]
