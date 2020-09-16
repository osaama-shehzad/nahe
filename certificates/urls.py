from django.urls import path

from . import views

app_name = "certificates"
urlpatterns = [
    path("", views.index, name="index"), 
    path("download/<str:name>/<str:date>", views.download, name="download")

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)