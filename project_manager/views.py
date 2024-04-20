from django.http import HttpResponse


def temporary_http_response(request):
    return HttpResponse("Temporary response for Project Manager?")
