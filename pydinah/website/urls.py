from django.urls import path
from .views import get_prediction, index


urlpatterns = [
    path('prediction/', get_prediction),
    path('', index, name='index')
]