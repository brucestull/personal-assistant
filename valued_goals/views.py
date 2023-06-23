from django.shortcuts import render


from django.http import HttpResponse

def index(request):
    return HttpResponse(
        f"Hello, world. You're at the valued_goals index."
        f"<br>"
        f"<a href='/'>Home</a>"
        )
    
