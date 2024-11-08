from django.urls import path
# creating a path 
from .views import *
urlpatterns = [
    path("",home),
    path("view/",view),
    path("send_email/",send_emaill),
]