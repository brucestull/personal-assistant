from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView
from .models import PiDevice
from .forms import PiDeviceForm


def pi_device_list(request):
    devices = PiDevice.objects.all()
    return render(request, 'pi_tracker/pi_device_list.html', {'devices': devices})


def pi_device_detail(request, pk):
    device = get_object_or_404(PiDevice, pk=pk)
    return render(request, 'pi_tracker/pi_device_detail.html', {'device': device})


class PiDeviceCreateView(CreateView):
    model = PiDevice
    form_class = PiDeviceForm
    template_name = 'pi_tracker/pi_device_form.html'

    def get_success_url(self):
        return reverse('pi_device_list')


class PiDeviceUpdateView(UpdateView):
    model = PiDevice
    form_class = PiDeviceForm
    template_name = 'pi_tracker/pi_device_form.html'

    def get_success_url(self):
        return reverse('pi_device_list')
