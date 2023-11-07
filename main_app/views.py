from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from .models import Usuario
from .forms import UserForm, LoginForm, MascotaForm, PreferenciasForm

# Superuser -> admin
# Password -> interpol1155

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")
#-----HOME VIEW-----*
def index(request): #Renderizar Paginas html aqui en views
    title = "Home"
    return render(request, "index.html",{
        'title' : title #Aqui le pase la variable que declare como title 
    })

#-----LOGIN VIEW-----*
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/') #Agregar la direccion del HOME
        
        else:
             messages.error(request,form.errors)
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form,
                                        'title' : "Login"})

#-----SIGNUP VIEW-----*
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Guardar el usuario en la base de datos
            user = form.save()
            # Autenticar al usuario y redirigirlo a otra vista
            login(request, user)
            return redirect('')  
        else:
             messages.error(request,form.errors)
    else:
        form = UserForm()
    return render(request,'Signup.html', {'form': form , 
                                        'title': "Sign up"})

#-----SIGNUP_MASCOTA VIEW-----*
def registro_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirige a la página de inicio después del registro
    else:
        form = UserForm()
    return render(request, 'registroMascota.html', {'form': form})

#-----PREFERENCIAS VIEW-----*

#-----LISTAUSUARIOS VIEW-----*
class ListaUsuariosView(ListView):
    model = Usuario
    template_name = 'lista.html'  
    context_object_name = 'usuarios'