from django.contrib.staticfiles.urls import urlpatterns
from django.urls import path
from metro.views import *



urlpatterns = [
    path('<int:pk>', GetStation.as_view()),#<int:pk>
    path('list/<str:page>/<int:limit>', GetListStations.as_view()),
    path('add', AddStation.as_view()),
    path('search', SearchStation.as_view())
]
