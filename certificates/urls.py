from django.urls import path

from . import views

app_name = "certificates"
urlpatterns = [
    path("", views.index, name="index"), 
    path("download/<str:date>/<str:name>/<str:graduation>/<str:id>", views.download, name="download"),
    path("sendrequest/<int:id>", views.sendrequest, name="sendrequest"),
    path("transcript/<int:cnic>", views.transcript, name="transcript")

]