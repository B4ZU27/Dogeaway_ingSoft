from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
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
    session_data = request.session.items()
    print("Información de la sesión:", session_data)
    mascota_seleccionada_id = request.session.get('mascota_seleccionada_id')

    # Si hay un ID de mascota seleccionada en la sesión, obtén la mascota desde la base de datos
    if mascota_seleccionada_id:
        mascota_seleccionada = get_object_or_404(Mascota, id=mascota_seleccionada_id)
    else:
        mascota_seleccionada = None
    return render(request, "index.html", {
        'title': title,
        'mascota_seleccionada': mascota_seleccionada,
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
            return redirect('mascotas/') #Agregar la direccion del HOME LOGEADO
    else:
        form = LoginForm()
    return render(request, 'Login.html', {'form': form})

#-----SIGNUP VIEW-----*
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('regitro_mascota')  # Redirige a la página de preferencias después del registro
    else:
        form = UserForm()
    return render(request,'Signup.html', {'form': form , 
                                        'title': "Sign up",
                                        'link': "{% static 'css/registros.css' %}"})

#-----PREFERENCIAS VIEW-----*
@login_required
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
        mascota_form = MascotaForm(request.POST)
        imagen_form = ImagenMascotaForm(request.POST, request.FILES)

        if mascota_form.is_valid():
            mascota = mascota_form.save(commit=False)
            mascota.dueño = request.user
            mascota.save()

            # Guardar las imágenes relacionadas con la mascota
            # imagenes = imagen_form.save(commit=False)
            # imagenes.mascota = mascota
            # imagenes.save()

            return redirect('mascotas_usuario')  # Redirige a la página principal de mascotas del usuario
        else:
            print("Formulario no válido")
            print(f"Errores en el formulario de mascota: {mascota_form.errors}")
            print(f"Errores en el formulario de imágenes: {imagen_form.errors}")
    else:
        mascota_form = MascotaForm()
        imagen_form = ImagenMascotaForm()

    return render(request, 'registroMascota.html', {'mascota_form': mascota_form, 'imagen_form': imagen_form})

#----ELEGIR MASCOTA-----*
@csrf_exempt
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

#----MATCH-----*
@login_required
def match_view(request):
    mascota_seleccionada_id = request.session.get('mascota_seleccionada_id')
    # Si hay un ID de mascota seleccionada en la sesión, obtén la mascota desde la base de datos
    if mascota_seleccionada_id:
        mascota_seleccionada = get_object_or_404(Mascota, id=mascota_seleccionada_id)
        usuario_id_actual = request.session.get('usuario.id')
        # Filtra las mascotas excluyendo aquellas que pertenecen al usuario actual
        lista_mascotas = Mascota.objects.exclude(dueño__id=usuario_id_actual)
    else:
        mascota_seleccionada = None
            # Redirige a la página de inicio después de seleccionar una mascota

    return render(request, 'Elegir_Mascota.html', {'mascota_selec': mascota_seleccionada, 'mascotas': lista_mascotas})

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


#Lista de ususarios
class ListaUsuariosView(ListView):
    model = Usuario
    template_name = 'lista.html'  # Reemplaza 'tu_app' con el nombre de tu aplicación
    context_object_name = 'usuarios'