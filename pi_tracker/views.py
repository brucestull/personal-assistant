from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import CreateView, UpdateView

from base.mixins import RegistrationAcceptedMixin
from base.decorators import registration_accepted_required

from .forms import PiDeviceForm
from .models import PiDevice


@registration_accepted_required
def pi_device_list(request):
    devices = PiDevice.objects.all()
    return render(request, 'pi_tracker/pi_device_list.html', {'devices': devices})


@registration_accepted_required
def pi_device_detail(request, pk):
    device = get_object_or_404(PiDevice, pk=pk)
    return render(request, 'pi_tracker/pi_device_detail.html', {'device': device})


class PiDeviceCreateView(RegistrationAcceptedMixin, CreateView):
    model = PiDevice
    form_class = PiDeviceForm
    template_name = 'pi_tracker/pi_device_form.html'

    def get_success_url(self):
        return reverse('pi_device_list')


class PiDeviceUpdateView(RegistrationAcceptedMixin, UpdateView):
    model = PiDevice
    form_class = PiDeviceForm
    template_name = 'pi_tracker/pi_device_form.html'

    def get_success_url(self):
        return reverse('pi_device_list')
