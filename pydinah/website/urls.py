from django.urls import path
from .views import get_prediction, index


urlpatterns = [
    path('', index, name='index'),
    path('prediction/', get_prediction),
]