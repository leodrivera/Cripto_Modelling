from django.urls import path
from .views import index, get_prediction, return_page


urlpatterns = [
    path('', index),
    path('prediction/', get_prediction),
    path('demo-plot/', return_page),
]