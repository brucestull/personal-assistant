from django.urls import path

from cbt.views import home


app_name = "cbt"
urlpatterns = [
    path(
        "",
        home,
        name="home",
    ),
]
