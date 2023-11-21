from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse
from .models import Usuario, Mascota, Match, Chat
from .forms import UserForm, LoginForm, MascotaForm, PreferenciasForm, ImagenMascotaForm, VerificacionForm, ReportesForm

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

            # Verifica si el usuario está verificado antes de redirigir
            if not user.verificado:
                messages.warning(request, 'Debes completar la verificación de identificación antes de iniciar sesión.')
                return redirect('verificacion')
            return redirect('mascotas_usuario')  # Corrige a la URL de inicio de sesión si es diferente
    else:
        form = LoginForm()
    return render(request, 'Login.html', {'form': form})

#-----SIGNUP VIEW-----*
def signup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()

            # Redirige a la página de verificación después del registro exitoso
            messages.success(request, 'Registro exitoso. Ahora procede con la verificación de identificación.')
            return redirect('verificacion')
    else:
        form = UserForm()
    return render(request, 'Signup.html', {'form': form, 'title': "Sign up", 'link': "{% static 'css/registros.css' %}"})

#-----VERIFICACION-----*
def verificacion(request):
    if request.method == 'POST':
        form = VerificacionForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            # Marcar al usuario como verificado después de enviar la foto de identificación
            request.user.verificado = True
            request.user.save()

            messages.success(request, 'Verificación exitosa. Ahora puedes iniciar sesión.')
            return redirect('login')
        else:
            messages.error(request, 'Hubo un problema con tu solicitud de verificación. Asegúrate de cargar una foto de identificación.')
    else:
        form = VerificacionForm(instance=request.user)
    return render(request, 'verificacion.html', {'form': form})

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
            return redirect('mascotas_usuario')
    else:
        form = ImagenMascotaForm()

    return render(request, 'registroImagenes_Mascota.html', {'form': form, 'mascota': mascota})

#-----EDITAR USUARIO-----*
class UsuarioUpdateView(UpdateView):
    model = Usuario
    template_name = 'usuario_actualizar.html'
    form_class = UserForm
    #fields = ['telefono', 'fecha_de_nacimiento', 'direccion'] #Agregar mas campos para editar

    def get_success_url(self):
        return reverse_lazy('home')

#-----ELIMINAR USUARIO-----*
class UsuarioDeleteView(DeleteView):
    model = Usuario
    template_name = 'usuario_eliminar.html'

    def get_success_url(self):
        return reverse_lazy('logout')

#-----DETALLE USUARIO-----
class UsuarioDetailView(DetailView):
    model = Usuario
    template_name = 'usuario_detalle.html'
    context_object_name = 'usuario'

    def get_object(self, queryset=None):
        return self.request.user  # Devuelve el usuario autenticado

    
#-----EDITAR MASCOTA-----*
class MascotaUpdateView(UpdateView):
    model = Mascota
    template_name = 'mascota_actualizar.html'
    fields = ['nombre', 'peso', 'sexo', 'tamaño', 'descripcion', 'raza', 'tiene_cartilla']

    def get_success_url(self):
        return reverse_lazy('home')

#-----ELIMINAR MASCOTA-----*
class MascotaDeleteView(DeleteView):
    model = Mascota
    template_name = 'mascota_eliminar.html'

    def get_success_url(self):
        return reverse_lazy('mascotas_usuario')

#-----DETALLE MASCOTA-----*
class MascotaDetailView(DetailView):
    model = Mascota
    template_name = 'mascota_detalle.html'
    context_object_name = 'mascota'

    def get_object(self, queryset=None):
        mascota_seleccionada_id = self.request.session.get('mascota_seleccionada_id')
        return get_object_or_404(Mascota, id=mascota_seleccionada_id, dueño=self.request.user)

#-----CHAT-----*
@login_required
def chat_view(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    mensajes = Chat.objects.filter(match=match).order_by('fecha_mensaje')

    if request.method == 'POST':
        mensaje = request.POST.get('mensaje')
        if mensaje:
            Chat.objects.create(
                match=match,
                remitente=request.user,
                mensaje=mensaje
            )
    return render(request, 'chat.html', {'match': match, 'mensajes': mensajes})

#-----REPORTAR USUARIO-----*
def reportar_usuario(request, usuario_id):
    usuario_reportado = get_object_or_404(Usuario, id=usuario_id)

    if request.method == 'POST':
        form = ReportesForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.reportador = request.user
            reporte.usuario_reportado = usuario_reportado
            reporte.save()
            return redirect('home')
    else:
        form = ReportesForm()

    return render(request, 'reportar_usuario.html', {'form': form, 'usuario_reportado': usuario_reportado})

#-----BLOQUEAR USUARIO-----*
@login_required
def bloquear_usuario(request, usuario_id):
    usuario_a_bloquear = get_object_or_404(Usuario, id=usuario_id)

    # Agregar el usuario a la lista de bloqueados
    request.user.usuarios_bloqueados.add(usuario_a_bloquear)

    # Bloquear los matches y chats existentes
    Match.objects.filter(mascota1__dueño=request.user, mascota2__dueño=usuario_a_bloquear).update(bloqueado=True)
    Match.objects.filter(mascota1__dueño=usuario_a_bloquear, mascota2__dueño=request.user).update(bloqueado=True)
    Chat.objects.filter(match__mascota1__dueño=request.user, match__mascota2__dueño=usuario_a_bloquear).update(bloqueado=True)
    Chat.objects.filter(match__mascota1__dueño=usuario_a_bloquear, match__mascota2__dueño=request.user).update(bloqueado=True)

    return redirect('home')

#-----DESBLOQUEAR USUARIO-----*
@login_required
def desbloquear_usuario(request, usuario_id):
    usuario_a_desbloquear = get_object_or_404(Usuario, id=usuario_id)

    # Eliminar al usuario de la lista de bloqueados
    request.user.usuarios_bloqueados.remove(usuario_a_desbloquear)

    return redirect('home')

#-----LISTA USUARIOS BLOQUEADOS-----*
@login_required
def lista_usuarios_bloqueados(request):
    usuarios_bloqueados = request.user.usuarios_bloqueados.all()
    return render(request, 'lista_usuarios_bloqueados.html', {'usuarios_bloqueados': usuarios_bloqueados})

#Lista de ususarios
class ListaUsuariosView(ListView):
    model = Usuario
    template_name = 'lista.html'  # Reemplaza 'tu_app' con el nombre de tu aplicación
    context_object_name = 'usuarios'