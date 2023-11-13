from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Usuario, Mascota
from .forms import UserForm, LoginForm, MascotaForm, PreferenciasForm, ImagenMascotaForm

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")

#-----INICIO-----*
def index(request): #Renderizar Paginas html aqui en views
    title = "Home"
    return render(request, "index.html",{
        'title' : title #Aqui le pase la variable que declare como title 
    })

#-----HOME-----*
@login_required
def home(request):
    return render(request, 'Home_Login.html')

#-----LOGIN VIEW-----*
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('mascotas_usuario') #Agregar la direccion del HOME
    else:
        form = LoginForm()
    return render(request, 'Login.html', {'form': form})

#-----SIGNUP VIEW-----*
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('preferencias')  # Redirige a la página de preferencias después del registro
    else:
        form = UserForm()
    return render(request,'Signup.html', {'form': form , 
                                        'title': "Sign up",
                                        'link': "{% static 'css/registros.css' %}"})

#-----PREFERENCIAS VIEW-----*
def preferencias(request):
    if request.method == 'POST':
        form = PreferenciasForm(request.POST)
        if 'submit_form' in request.POST:
            if form.is_valid():
                form.save()
        return redirect('/')  # Redirige a la página de inicio después del registro o si se omite el formulario
    else:
        form = PreferenciasForm()
    return render(request, 'Preferencias.html', {'form': form})

#-----SIGNUP_MASCOTA VIEW-----*
@login_required
def registro_mascota(request):
    if request.method == 'POST':
        form = MascotaForm(request.POST)
        if form.is_valid():
            mascota = form.save(commit=False)
            mascota.dueño = request.user
            mascota.save()
            return redirect('cargar_imagenes_mascota', mascota_id=mascota.id)  # Redirige a la carga de imágenes con la ID de la mascota
    else:
        form = MascotaForm()
    return render(request, 'registroMascota.html', {'form': form})

#----ELEGIR MASCOTA-----*
@login_required
def mascotas_usuario(request):
    mascotas = Mascota.objects.filter(dueño=request.user)

    if request.method == 'POST':
        mascota_id = request.POST.get('mascota_id')
        if mascota_id:
            # Almacena la mascota seleccionada en la sesión
            request.session['mascota_seleccionada_id'] = mascota_id

            # Redirige a la página de inicio después de seleccionar una mascota
            return redirect('home')

    return render(request, 'Elegir_Mascota.html', {'mascotas': mascotas})

#----IMAGENES MASCOTA-----*
@login_required
def cargar_imagenes_mascota(request, mascota_id):
    mascota = get_object_or_404(Mascota, id=mascota_id, dueño=request.user)

    if request.method == 'POST':
        form = ImagenMascotaForm(request.POST, request.FILES)
        if form.is_valid():
            imagenes_mascota = form.save(commit=False)
            imagenes_mascota.mascota = mascota
            imagenes_mascota.save()
            return redirect('mascotas_usuario')  # Redirige a la siguiente página después de cargar las imágenes
    else:
        form = ImagenMascotaForm()

    return render(request, 'registroImagenes_Mascota.html', {'form': form, 'mascota': mascota})

#-----LISTAUSUARIOS VIEW-----*
def lista_usuarios(request):
    return render(request, 'listaUsuarios.html')

#Lista de ususarios
class ListaUsuariosView(ListView):
    model = Usuario
    template_name = 'main_app/listaUsuarios.html'  # Reemplaza 'tu_app' con el nombre de tu aplicación
    context_object_name = 'usuarios'