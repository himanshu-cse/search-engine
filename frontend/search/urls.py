from django.urls import path
from .views import search_view, analytics_view

urlpatterns = [
    path("", search_view, name="search"),
    path("analytics/", analytics_view, name="analytics")
]