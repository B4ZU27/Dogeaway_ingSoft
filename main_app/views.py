from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegistroForm, RegistroMascotaForm

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")

def index(request): #Renderizar Paginas html aqui en views
    title = "Te mando este titulo por parametro we"
    return render(request, "index.html",{
        'title' : title #Aqui le pase la variable que declare como title 
    })

def signup(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pagina_de_inicio')  # Redirige a la página de inicio después del registro
    else:
        form = RegistroForm()
    return render(request, 'Signup.html', {'form': form})

def registro_mascota(request):
    if request.method == 'POST':
        form = RegistroMascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pagina_de_inicio')  # Redirige a la página de inicio después del registro
    else:
        form = RegistroForm()
    return render(request, 'registroMascota.html', {'form': form})