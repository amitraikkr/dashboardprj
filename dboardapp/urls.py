from django.urls import path
from dboardapp.views import dashboard

urlpatterns = [
	path('', dashboard, name="home"),
]