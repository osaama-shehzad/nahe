from django.urls import path

from . import views

app_name = "certificates"
urlpatterns = [
    path("", views.index, name="index"), 
    path("download/<str:name>/<str:date>/<str:id>", views.download, name="download"),
    path("sendrequest/<int:id>", views.sendrequest, name="sendrequest"),
    path("transcript/<str:cnic>", views.transcript, name="transcript")

]