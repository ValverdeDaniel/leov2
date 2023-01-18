from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='options'),
    path('<ticker>', views.ticker_view, name='ticker'),
    # path('option', views.index, name='option')

]