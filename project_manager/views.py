from django.http import HttpResponse

from base.decorators import registration_accepted_required


@registration_accepted_required
def temporary_http_response(request):
    return HttpResponse("Temporary response for Project Manager?")
