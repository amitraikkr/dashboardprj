from django.urls import path
from dboardapp.views import dashboard,graph_view

urlpatterns = [
	path('', dashboard, name="home"),
	path('graphvw/',graph_view,name="graphvw"),
]