from django.urls import path
from . import views

urlpatterns = [
    path('', views.trace, name='trace'),
    path('predict-route/', views.predict, name='predict')
]