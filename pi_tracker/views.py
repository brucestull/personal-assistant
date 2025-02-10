from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, UpdateView

from base.decorators import registration_accepted_required
from base.mixins import RegistrationAcceptedMixin
from config.settings import THE_SITE_NAME

from .forms import PiDeviceForm
from .models import PiDevice


@registration_accepted_required
def pi_device_list(request):
    devices = PiDevice.objects.all()
    return render(
        request,
        "pi_tracker/pi_device_list.html",
        {
            "devices": devices,
            "the_site_name": THE_SITE_NAME,
            "page_title": "Pi Devices",
        },
    )


@registration_accepted_required
def pi_device_detail(request, pk):
    device = get_object_or_404(PiDevice, pk=pk)
    return render(
        request,
        "pi_tracker/pi_device_detail.html",
        {
            "device": device,
            "the_site_name": THE_SITE_NAME,
        },
    )


class PiDeviceCreateView(RegistrationAcceptedMixin, CreateView):
    model = PiDevice
    form_class = PiDeviceForm
    template_name = "pi_tracker/pi_device_form.html"
    extra_context = {
        "the_site_name": THE_SITE_NAME,
    }

    # This is handled in the model's `get_absolute_url` method.
    # def get_success_url(self):
    #     return reverse("pi_tracker:pi_device_list")


class PiDeviceUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = PiDevice
    form_class = PiDeviceForm
    template_name = "pi_tracker/pi_device_form.html"
    extra_context = {
        "the_site_name": THE_SITE_NAME,
    }

    # This is handled in the model's `get_absolute_url` method.
    # def get_success_url(self):
    #     return reverse("pi_tracker:pi_device_list")
