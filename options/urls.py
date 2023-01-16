from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='options'),
    path('filterStocks', views.filterStocks, name='filterStocks')
]