from django.http import HttpResponse, JsonResponse


def json_response(request):
    """
    View function for the `json_response` view.
    """
    return JsonResponse(
        {
            "message": "Goodbuy, World! Enjoy the sails and bar guns!",
            "status": 200,
        }
    )
