from django.http import HttpResponse


def temp_index(request):
    return HttpResponse("Hello, world. You're at the temp index!")
