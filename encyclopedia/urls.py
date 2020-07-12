from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wikipage, name ="wikipage"),
    path("search", views.search, name ="search"),
    path("new", views.new, name ="new"),
    path("edit/<str:title>", views.edit, name ="edit"),
    path("edited", views.edited, name ="edited"),
    path("random_page", views.random_page, name ="random_page")
]