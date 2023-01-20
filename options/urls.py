from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='options'),
    path('clear_cache', views.clear_cache, name='clear_cache'),
    path('<ticker>', views.ticker_view, name='ticker'),
    
    # path('option', views.index, name='option')

]