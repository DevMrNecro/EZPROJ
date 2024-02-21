from django.urls import path, include
from .views import MqttListener

urlpatterns = [
    path('mqtt-listener/', MqttListener.as_view(), name='mqtt-listener')
]
