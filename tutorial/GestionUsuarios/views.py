from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import funcionario
from django.contrib.auth.decorators import login_required
from  django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from .forms import Tipos_Usuario_form
from tutorial.GestionSistema.views import usuario_main


# Create your views here.
@login_required(login_url="/login/")
def crear_usuario_view(request):
    """
    Redirecciona a la interfaz para la creacion de un usuario nuevo
    """
    grupo_de_permisos = Group.objects.all()
    usuario_sesion = usuario_main(request)
    #Primero creara un usuario de forma temporal para poder asignar los
    #permisos que sean elegidos
    if request.method == 'POST' and 'Guardar' in request.POST:
        username = request.POST.get('username')
        password = make_password(request.POST.get('password'), salt=None,
            hasher='default')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        telefono_2 = request.POST.get('telefono_2')
        direccion = request.POST.get('direccion')
        activo = request.POST.get('activo')
        roles_asignados = request.POST.getlist('agregar')

        #Controla que el usuario a crear sea unico
        if User.objects.filter(username=username).exists():
            return render_to_response("Gestion_de_usuarios/crear_usuario.html",
                                      {'error': 'existente',
                                          'usuario_sesion': usuario_sesion,
                                          'disponibles': grupo_de_permisos},
                                      context_instance=RequestContext(request))

        #Controlara que se haya seleccionado al menos un rol
        if len(roles_asignados) == 0:
            return render_to_response("Gestion_de_usuarios/crear_usuario.html",
                                      {'error': 'roles',
                                          'usuario_sesion': usuario_sesion,
                                          'disponibles': grupo_de_permisos},
                                      context_instance=RequestContext(request))
        #Controla que no se hayan dejado en blanco ningun campo
        if username != '' and password != '' and lastname != '' and \
        firstname != '':
            # Se creara el usuario
            user = funcionario(username=username, password=password,
                correo=correo, telefono=telefono, telefono_2=telefono_2)
            user.first_name = firstname
            user.last_name = lastname
            user.direccion = direccion

            #Si no se elige una de las opciones se tomara usuario desactivado
            #por defecto
            if activo == 'true':
                user.is_active = True
            else:
                user.is_active = False

            user.is_staff = True
            user.is_superuser = False
            user.save()
            #Se agrega el rol que poseera el usuario
            for item in roles_asignados:
                group = Group.objects.get(pk=item)
                user.groups.add(group)

            return HttpResponseRedirect('/listar_usuarios/')
            #return render_to_response("Gestion_de_usuarios/crear_usuario.html"
                # ,{'error': 'ninguno',  'disponibles': grupo_de_permisos},
                #context_instance=RequestContext(request))
        else:
            return render_to_response("Gestion_de_usuarios/crear_usuario.html",
                {'error': 'vacio', 'disponibles': grupo_de_permisos,
                    'usuario_sesion': usuario_sesion},
                context_instance=RequestContext(request))
    return render_to_response("Gestion_de_usuarios/crear_usuario.html",
        {'disponibles': grupo_de_permisos, 'usuario_sesion': usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def listar_usuarios_view(request):
    """
    Permite al usuario realizar el listado de usuarios que se encuentran en el
    sistema habilitando con la opcion de filtrados de usuarios, tambien
    habilitara el boton para modificar, crear o eliminar si es que posee los
    permisos el usuario en sesion
    """
    tipos = {}
    usuario_sesion = usuario_main(request)
    if request.method == 'POST':
        form = Tipos_Usuario_form(request.POST)
        if form.is_valid():
            tipos = form.cleaned_data.get('Tipos_Usuario')
            busqueda = form.cleaned_data.get('Busqueda')
            #Si el usuario ingresa "Todos"
            if busqueda == 'todos' or busqueda == 'Todos':
                usuarios = User.objects.filter(is_active='True').order_by(
                    'username')
                context = {'form': form, 'usuarios': usuarios}
            #Si el usuario ingresa un tipo y un nombre especificos
            elif busqueda != '' and tipos:
                usuarios = \
                User.objects.filter(groups__id=tipos.id).\
                filter(username=busqueda, is_active='True').order_by('username')
                context = {'form': form, 'usuarios': usuarios}
            elif tipos:  # Si el usuario solo ingresa el tipo
                usuarios = User.objects.filter(groups__id=tipos.id,
                is_active='True').order_by('username')
                context = {'form': form, 'usuarios': usuarios}
            elif busqueda != '' and not tipos:  # Si el usuario ingresa
            #solo el nombre
                usuarios = User.objects.filter(username=busqueda,
                is_active='True').order_by('username')
                context = {'form': form, 'usuarios': usuarios}
            else:
                form = Tipos_Usuario_form()
                #tipos = "Ninguno" Es cuando el usuario oprime el boton buscar
                #sin ningun parametro de busqueda
                context = {'form': form}
        else:
            form = Tipos_Usuario_form()
            #tipos = "No valido" Es cuando el parametro de busqueda es invalido
            context = {'form': form}

    else:
        form = Tipos_Usuario_form()
        usuarios = User.objects.filter(is_active='True').order_by('username')

        context = {'form': form, 'usuarios': usuarios,
            'usuario_sesion': usuario_sesion}
    return render(request, 'Gestion_de_usuarios/listar_usuarios.html',
        context)


@login_required(login_url="/login/")
def modificar_usuario_view(request, id_usuario):
    """
    Redirecciona al usuario la modificacion de un usuario especifico
    :param id_usuario: el id del usuario que sera modificado
    :return:
    """
    grupos_permisos = Group.objects.all()
    usuario_sesion = usuario_main(request)

    #Se obtienen los datos del usuario
    usuario_seleccionado = funcionario.objects.get(pk=id_usuario)
#    usuario_seleccionado = funcionario.objects.get(pk=id_usuario)
    roles_asignados = usuario_seleccionado.groups.all()
    usuario_pass_hash = usuario_seleccionado.password

    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_usuarios/')

    if request.method == 'POST' and 'Guardar' in request.POST:
        usuario_seleccionado.username = request.POST.get('username')
        usuario_seleccionado.first_name = request.POST.get('firstname')
        usuario_seleccionado.telefono = request.POST.get('telefono')
        usuario_seleccionado.telefono_2 = request.POST.get('telefono_2')
        usuario_seleccionado.direccion = request.POST.get('direccion')
        usuario_seleccionado.password = request.POST.get('password')
        usuario_seleccionado.last_name = request.POST.get('lastname')
        usuario_seleccionado.correo = request.POST.get('correo')
        roles_asignados = request.POST.getlist('agregar')

        if request.POST.get('activo'):
            usuario_seleccionado.is_active = True
        else:
            usuario_seleccionado.is_active = False

        #Controlara que se haya asignado un rol como minimo al modificar
        if len(roles_asignados) == 0:
            return render_to_response("GestionUsuarios/modificar_usuario.html",
                                      {'error': "roles",
                                          'usuario': usuario_seleccionado,
                                          'grupos': grupos_permisos,
                                          'roles': roles_asignados},
                                              context_instance=
                                              RequestContext(request))

            #Controla que no se hayan dejado en blanco ningun campo
        if usuario_seleccionado.username != '' \
        and usuario_seleccionado.password != '' \
        and usuario_seleccionado.last_name != '' \
        and usuario_seleccionado.first_name != '' \
        and usuario_seleccionado.telefono != '' \
        and usuario_seleccionado.direccion != '':
            usuario_seleccionado.groups.clear()
            #Se agrega el rol que poseera el usuario
            for item in roles_asignados:
                group = Group.objects.get(pk=item)
                usuario_seleccionado.groups.add(group)

            if usuario_seleccionado.password != usuario_pass_hash:
                usuario_seleccionado.password = \
                make_password(usuario_seleccionado.password,
                salt=None, hasher='default')

            usuario_seleccionado.save()
            return HttpResponseRedirect('/listar_usuarios/')
        else:
            return render_to_response(
                "Gestion_de_usuarios/modificar_usuario.html",
                                      {'error': "vacio",
                                      'usuario': usuario_seleccionado,
                                      'grupos': grupos_permisos,
                                      'roles': roles_asignados},
                                          context_instance=
                                          RequestContext(request))

    return render_to_response("Gestion_de_usuarios/modificar_usuario.html",
                              {"usuario": usuario_seleccionado,
                                  'grupos': grupos_permisos,
                                  'roles': roles_asignados,
                                  'usuario_sesion': usuario_sesion},
                                      context_instance=RequestContext(request))


@login_required(login_url="/login/")
def consultar_usuario_view(request, id_usuario):
    usuario_seleccionado = funcionario.objects.get(pk=id_usuario)
    usuario_sesion = usuario_main(request)
    roles_asignados = usuario_seleccionado.groups.values_list('name', flat=True)
    rol = roles_asignados[0]
    return render_to_response("Gestion_de_usuarios/consultar_usuario.html",
        {"usuario": usuario_seleccionado, 'roles': rol,
            'usuario_sesion': usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def eliminar_usuario_view(request, id_usuario):
    """
    La funcion Eliminar en realidad solo cambia el estado del usuario en
    la base de datos dejandolo inactivo, a fin de tener un registro sobre el
    historial de los usuarios creados.
    """
    usuario_seleccionado = funcionario.objects.get(pk=id_usuario)
    username = usuario_seleccionado.username
    usuario_sesion = usuario_main(request)
    if request.method == 'POST' and 'Aceptar' in request.POST:
        usuario_seleccionado.is_active = False
        usuario_seleccionado.save()
        return HttpResponseRedirect('/listar_usuarios/')
    elif request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_usuarios/')
    else:
        return render_to_response('Gestion_de_usuarios/eliminar_usuario.html',
            {'username': username,
                'usuario_sesion': usuario_sesion}, RequestContext(request))

@login_required(login_url="/login/")                
def cambiar_password_view(request):
    usuario_sesion = usuario_main(request)
    if request.method == 'POST' and 'Guardar' in request.POST:
        print request.POST.get('password')
        usuario_sesion.password = make_password(request.POST.get('password'), salt=None,
            hasher='default')
        usuario_sesion.save()
        return HttpResponseRedirect('/listar_usuarios/')
    return render_to_response('Gestion_de_usuarios/cambiar_password.html', {'usuario_sesion':usuario_sesion}, RequestContext(request))
