
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', hello),
    path('themFind/', find),
    path('news/', NewsView.as_view()),
    path('news/<theme>/', NewsView.as_view()),
    path('user_check/', UserCheck.as_view()),
    path('users/<int:pk>', UserView.as_view()),
    path('users/', UserView.as_view()),
]
