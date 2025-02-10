from django.urls import path

from . import views

app_name = "pi_tracker"
urlpatterns = [
    path("", views.pi_device_list, name="pi_device_list"),
    path("<int:pk>/", views.pi_device_detail, name="pi_device_detail"),
    path("create/", views.PiDeviceCreateView.as_view(), name="pi_device_create"),
    path(
        "<int:pk>/update/", views.PiDeviceUpdateView.as_view(), name="pi_device_update"
    ),
]
