from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")

def index(request): #Renderizar Paginas html aqui en views
    title = "Te mando este titulo por parametro we"
    return render(request, "index.html",{
        'title' : title #Aqui le pase la variable que declare como title 
    })

