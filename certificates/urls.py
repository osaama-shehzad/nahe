from django.urls import path

from . import views

app_name = "certificates"
urlpatterns = [
    path("", views.index, name="index"), 
    path("search", views.search, name="search"),
    path("download/<str:date>/<str:name>/<str:graduation>/<str:id>", views.download, name="download"),
    path("sendrequest", views.sendrequest, name="sendrequest")
]