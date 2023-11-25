from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from django.views.generic import DetailView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from .models import Usuario, Mascota, Match, Chat
from .forms import UserForm, LoginForm, MascotaForm, PreferenciasForm, ImagenMascotaForm, VerificacionForm, ReportesForm, UserEditForm, MascotaEditForm

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
            request.session['usuario_no_verificado'] = user.id
            #login(request, user)
            # Redirige a la página de verificación después del registro exitoso
            messages.success(request, 'Registro exitoso. Ahora procede con la verificación de identificación.')
            return redirect('verificacion')
       
    else:
        form = UserForm()
    return render(request, 'Signup.html', {'form': form, 'title': "Sign up", 'link': "{% static 'css/registros.css' %}"})

#-----VERIFICACION-----*
def verificacion(request):
    usuario_vr_id = request.session.get('usuario_no_verificado')
    if usuario_vr_id is not None:
        usuario_vr = get_object_or_404(Usuario, id=usuario_vr_id)
        form = VerificacionForm(request.POST, request.FILES, instance=usuario_vr)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                # Marcar al usuario como verificado después de enviar la foto de identificación
                #si viene del signup 
                usuario_vr.verificado = True
                usuario_vr.save()
                messages.success(request, 'Verificación exitosa. Ahora puedes iniciar sesión.')
                return redirect('/')
            else:
                messages.error(request, 'Hubo un problema con tu solicitud de verificación. Asegúrate de cargar una foto de identificación.')
    else:
        #viene del login
        form = VerificacionForm(instance=request.user)
        if request.method == 'POST':
            if form.is_valid():
                request.user.verificado = True
                request.user.save()
                messages.success(request, 'Verificación exitosa.')
                return redirect('/')
            else:
                messages.error(request, 'Hubo un problema con tu solicitud de verificación. Asegúrate de cargar una foto de identificación.') 
    return render(request, 'verificacion.html', {'form': form})

#-----PREFERENCIAS VIEW-----*
@login_required
def preferencias(request):
    if request.method == 'POST':
        form = PreferenciasForm(request.POST)
        if 'submit_form' in request.POST:
            if form.is_valid():
                form.save()
        return redirect('mascotas_usuario')  # Redirige a la página de inicio después del registro o si se omite el formulario
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
            #imagenes = imagen_form.save(commit=False)
            #imagenes.mascota = mascota
            #imagenes.save()

            return redirect('mascotas_usuario')  # Redirige a la página principal de mascotas del usuario
        else:
            print("Formulario no válido")
            print(f"Errores en el formulario de mascota: {mascota_form.errors}")
            print(f"Errores en el formulario de imágenes: {imagen_form.errors}")
    else:
        mascota_form = MascotaForm()
        imagen_form = ImagenMascotaForm()

    return render(request, 'registroMascota.html', {'title':"Registro Mascota",'mascota_form': mascota_form, 'imagen_form': imagen_form})

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

    return render(request, 'Elegir_Mascota.html', {'title':"Elegir Mascota",'mascotas': mascotas})

#----MATCH-----*
@login_required
def match_view(request):
    mascota_seleccionada_id = request.session.get('mascota_seleccionada_id')
    # Si hay un ID de mascota seleccionada en la sesión, obtén la mascota desde la base de datos
    if mascota_seleccionada_id:
        mascota_seleccionada = get_object_or_404(Mascota, id=mascota_seleccionada_id)
        print('Nombre - '+mascota_seleccionada.nombre)
        # Filtra las mascotas excluyendo aquellas que pertenecen al usuario actual
        lista_mascotas = Mascota.objects.exclude(sexo=mascota_seleccionada.sexo)

        for mascota in lista_mascotas:
            print('{- '+mascota.nombre+'|'+mascota.sexo+'>'+str(mascota.id))
    else:
        mascota_seleccionada = None
        redirect('/')
        # Redirige a la página de inicio si no obtiene el objeto

    return render(request, 'match.html', { 
        'title': "Match",
        'mascota_selec': mascota_seleccionada,
        'mascotas': lista_mascotas})
 # - - - LIKE_MASCOTA - - - #
def like_mascota(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        mascota_id = request.POST.get('mascota_id')
        mascota_seleccionada_id = request.session.get('mascota_seleccionada_id')

        if mascota_seleccionada_id:# SI HAY UNA MASCOTA SELECCIONADA
            mascota_seleccionada = get_object_or_404(Mascota, id=mascota_seleccionada_id)#Conseguir la mascota
            mascota_liked = mascota_seleccionada.liked_by.filter(id=mascota_id).first()#conseguir el like

            if mascota_liked:
                # Si ya le dio like a nuestra mascota, MATCH
                response_data = {'status': 'MATCH', 'message': '¡MATCH!'}
                #print('match')
                # Crear el Match
                nuevo_match = Match.objects.create(mascota1=mascota_seleccionada, mascota2=get_object_or_404(Mascota, id=mascota_id))
                #Borramos el like
                mascota_seleccionada.liked_by.remove(mascota_liked)
                #messages.success(request, '!! MATCH !!')
            else:
                # Si no dio like, agregamos mascota a esa mascota
                mascota = get_object_or_404(Mascota, id=mascota_id)
                if(mascota.liked_by.filter(id=mascota_seleccionada_id)):
                    response_data = {'status': 'like_added_already', 'message': 'Ya hay un like otorgado'}
                    messages.info(request, 'Ya se habia dado like')
                    #print('ya se habia dado')
                else:
                    mascota.liked_by.add(mascota_seleccionada) # revisa que pedo con esto 
                    response_data = {'status': 'like_added','message': 'Se agrego un like'}
                    #print('like agregado')
                    #messages.success(request, 'Like agregado')

        return JsonResponse(response_data)


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

#-----DETALLE USUARIO-----*
class VerInformacionUsuario(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'usuario_detalle.html'
    context_object_name = 'usuario'

    def get_object(self, queryset=None):
        return self.request.user

#-----EDITAR USUARIO-----*
@login_required
def ActualizarInformacionUsuario(request):
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Información actualizada exitosamente.')
            return redirect('ver_informacion_usuario')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'usuario_actualizar.html', {'form': form})

#-----ELIMINAR USUARIO-----*
class EliminarCuentaUsuario(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'usuario_eliminar.html'
    success_url = reverse_lazy('logout')

    def get_object(self, queryset=None):
        return self.request.user

#-----DETALLE MASCOTA-----*
class VerDetalleMascota(LoginRequiredMixin, DetailView):
    model = Mascota
    template_name = 'mascota_detalle.html'
    context_object_name = 'mascota'

    def get_object(self, queryset=None):
        mascota_id = self.kwargs.get('mascota_id')
        return get_object_or_404(Mascota, id=mascota_id, dueño=self.request.user)

#-----EDITAR MASCOTA-----*
@login_required
def ActualizarInformacionMascota(request, mascota_id):
    mascota = Mascota.objects.get(pk=mascota_id)

    if request.method == 'POST':
        form = MascotaEditForm(request.POST, instance=mascota)
        if form.is_valid():
            form.save()
            messages.success(request, 'Mascota actualizada exitosamente.')
            return redirect('ver_detalle_mascota', mascota_id=mascota_id)
    else:
        form = MascotaEditForm(instance=mascota)

    return render(request, 'mascota_actualizar.html', {'form': form, 'mascota': mascota})

#-----ELIMINAR MASCOTA-----*
class EliminarMascota(LoginRequiredMixin, DeleteView):
    model = Mascota
    template_name = 'mascota_eliminar.html'
    success_url = reverse_lazy('mascotas_usuario')

    def get_object(self, queryset=None):
        mascota_id = self.kwargs.get('mascota_id')
        return get_object_or_404(Mascota, id=mascota_id, dueño=self.request.user)

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
    template_name = 'lista.html'  
    context_object_name = 'usuarios'