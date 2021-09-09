from django.urls import path, include
from .views import PredictionModels

urlpatterns = [
    path('<pk>/<model>/',PredictionModels),#get request
]
