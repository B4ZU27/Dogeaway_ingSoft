from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import UserForm, LoginForm, MascotaForm, PreferenciasForm

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")

def index(request): #Renderizar Paginas html aqui en views
    title = "Te mando este titulo por parametro we"
    return render(request, "index.html",{
        'title' : title #Aqui le pase la variable que declare como title 
    })

#-----LOGIN VIEW-----*
def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('') #Agregar la direccion del HOME
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

#-----SIGNUP VIEW-----*
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pagina_de_inicio')  # Redirige a la página de inicio después del registro
    else:
        form = UserForm()
    return render(request, 'Signup.html', {'form': form})

#-----SIGNUP_MASCOTA VIEW-----*
def registro_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pagina_de_inicio')  # Redirige a la página de inicio después del registro
    else:
        form = UserForm()
    return render(request, 'registroMascota.html', {'form': form})

#-----PREFERENCIAS VIEW-----*