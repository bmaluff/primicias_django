from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from .models import cliente, direccionesXcliente
#from django.contrib.auth.decorators import login_required
from .forms import Tipos_Usuario_form
from django.db.models import Q
from tutorial.GestionDelivery.models import zona
from tutorial.GestionSistema.views import usuario_main
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="/login/")
def crear_cliente_view(request):
    """
    Redirecciona a la interfaz para la creacion de un usuario nuevo
    """
    # Primero creara un usuario de forma temporal para poder asignar los
    # permisos que sean elegidos
    usuario_sesion = usuario_main(request)
    if request.method == 'POST' and 'Guardar' in request.POST:
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')
        telefono_2 = request.POST.get('telefono_2')
        direcciones = request.POST.getlist('direcciones')
        ruc_ci = request.POST.get('ruc_ci')
        zonas = request.POST.getlist('zonas')
        # Controla que el usuario a crear sea unico
        # if User.objects.filter(username=username).exists():
        # return render_to_response("Gestion_de_usuarios/crear_usuario.html",
        #                        {'error': 'existente',
        #                                  'disponibles': grupo_de_permisos},
        #                              context_instance=RequestContext(request))

        # Controlara que se haya seleccionado al menos un rol
        # if len(roles_asignados) == 0:
        #   return render_to_response("Gestion_de_usuarios/crear_usuario.html",
        #                              {'error': 'roles',
        #                                  'disponibles': grupo_de_permisos},
        #                              context_instance=RequestContext(request))
        # Controla que no se hayan dejado en blanco ningun campo
        if nombre != '' and apellido != '' and direcciones != '' and \
        telefono != '':
            # Se creara el cliente
            nuevo = cliente(correo=correo, telefono=telefono,
                telefono_2=telefono_2, nombre=nombre,
            apellido=apellido, ruc_ci=ruc_ci)

            nuevo.save()

            for indice, elemento in enumerate(direcciones):
                nuevaDireccion = direccionesXcliente(
                    cliente=cliente.objects.get(pk=nuevo.id),
                    direccion=elemento, zona=zonas[indice]
                    )
                nuevaDireccion.save()
            #Se agrega el rol que poseera el usuario
            return HttpResponseRedirect('/listar_clientes/')
        else:
            nuevo = cliente(correo=correo, telefono=telefono,
                telefono_2=telefono_2, nombre=nombre,
            apellido=apellido, direccion=direccion, ruc_ci=ruc_ci,
            direccion2=direccion2)
            return render_to_response("Gestion_de_clientes/crear_cliente.html",
                {'error': 'vacio', 'usuario': nuevo,
                    'usuario_sesion': usuario_sesion},
                context_instance=RequestContext(request))
    zonas = zona.objects.filter(is_active=True)
    return render_to_response("Gestion_de_clientes/crear_cliente.html",
        {'zonas': zonas, 'usuario_sesion': usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def listar_clientes_view(request):
    """
    Permite al usuario realizar el listado de usuarios que se encuentran en el
    sistema habilitando con la opcion de filtrados de usuarios, tambien
    habilitara el boton para modificar, crear o eliminar si es que posee los
    permisos el usuario en sesion
    """
    usuario_sesion = usuario_main(request)
    if request.method == 'POST':
        form = Tipos_Usuario_form(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data.get('Busqueda')
            #Si el usuario ingresa "Todos"
            if busqueda == 'todos' or busqueda == 'Todos':
                clientes = cliente.objects.filter(
                    is_active='True').order_by('nombre', 'apellido')
                context = {'form': form, 'clientes': clientes,
                    'usuario_sesion': usuario_sesion}
            #Si el usuario ingresa un tipo y un nombre especificos
            elif busqueda != '':
                clientes = \
                cliente.objects.filter(Q(nombre__icontains=busqueda) |
                Q(apellido__icontains=busqueda) |
                Q(telefono__icontains=busqueda) |
                Q(telefono_2__icontains=busqueda)).order_by('nombre')
                context = {'form': form, 'clientes': clientes,
                    'usuario_sesion': usuario_sesion}
            else:
                form = Tipos_Usuario_form()
                #tipos = "Ninguno" Es cuando el usuario oprime el boton buscar
                #sin ningun parametro de busqueda
                context = {'form': form}
        else:
            form = Tipos_Usuario_form()
            #tipos = "No valido" Es cuando el parametro de busqueda es invalido
            context = {'form': form, 'usuario_sesion': usuario_sesion}

    else:
        form = Tipos_Usuario_form()
        clientes = cliente.objects.filter(is_active='True').order_by('nombre',
            'apellido')

        context = {'form': form, 'clientes': clientes,
            'usuario_sesion': usuario_sesion}
    return render(request, 'Gestion_de_clientes/listar_clientes.html',
        context)


@login_required(login_url="/login/")
def modificar_cliente_view(request, id_cliente):
    """
    Redirecciona al usuario la modificacion de un usuario especifico
    :param id_usuario: el id del usuario que sera modificado
    :return:
    """
    usuario_sesion = usuario_main(request)
    # Se obtienen los datos del usuario
    cliente_seleccionado = cliente.objects.get(pk=id_cliente)
    direccionesActuales = direccionesXcliente.objects.filter(
        cliente_id=cliente_seleccionado)
#    usuario_seleccionado = funcionario.objects.get(pk=id_usuario)

    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_clientes/')

    if request.method == 'POST' and 'Guardar' in request.POST:
        cliente_seleccionado.nombre = request.POST.get('nombre')
        cliente_seleccionado.telefono = request.POST.get('telefono')
        cliente_seleccionado.telefono_2 = request.POST.get('telefono_2')
        cliente_seleccionado.apellido = request.POST.get('apellido')
        cliente_seleccionado.correo = request.POST.get('correo')
        cliente_seleccionado.ruc_ci = request.POST.get('ruc_ci')
        direccionesNuevas = request.POST.getlist('direcciones')
        zonasNuevas = request.POST.getlist('zonas')
            #Controla que no se hayan dejado en blanco ningun campo
        if cliente_seleccionado.apellido != '' \
        and cliente_seleccionado.nombre != '' \
        and cliente_seleccionado.telefono != '' \
        and direccionesNuevas != '':

            cliente_seleccionado.save()
            direccionesActuales.delete()
            for indice, elemento in enumerate(direccionesNuevas):
                nuevaDireccion = direccionesXcliente(
                    cliente=cliente_seleccionado,
                    direccion=elemento, zona=zonasNuevas[indice]
                    )
                nuevaDireccion.save()

            return HttpResponseRedirect('/listar_clientes/')
        else:
            return render_to_response(
                "Gestion_de_clientes/modificar_cliente.html",
                {'error': "vacio", 'cliente': cliente_seleccionado,
                 'usuario_sesion': usuario_sesion},
                context_instance=RequestContext(request))
    zonas = zona.objects.filter(is_active=True)
    return render_to_response("Gestion_de_clientes/modificar_cliente.html",
                              {"cliente": cliente_seleccionado, 'zonas': zonas,
                                  'usuario_sesion': usuario_sesion,
                                  'direccionesActuales': direccionesActuales},
                              context_instance=RequestContext(request))


@login_required(login_url="/login/")
def consultar_cliente_view(request, id_cliente):
    cliente_seleccionado = cliente.objects.get(pk=id_cliente)
    usuario_sesion = usuario_main(request)
    direccionesActuales = direccionesXcliente.objects.filter(
        cliente_id=cliente_seleccionado)
    if request.method == 'POST' and 'Retroceder' in request.POST:
        return HttpResponseRedirect('/listar_clientes/')
    return render_to_response("Gestion_de_clientes/consultar_cliente.html",
                              {"cliente": cliente_seleccionado,
                               'direccionesActuales': direccionesActuales,
                               'usuario_sesion': usuario_sesion},
                              context_instance=RequestContext(request))


@login_required(login_url="/login/")
def eliminar_cliente_view(request, id_cliente):
    """
    La funcion Eliminar en realidad solo cambia el estado del cliente en
    la base de datos dejandolo inactivo, a fin de tener un registro sobre el
    historial de los clientes creados.
    """
    usuario_sesion = usuario_main(request)
    cliente_seleccionado = cliente.objects.get(pk=id_cliente)
    if request.method == 'POST' and 'Aceptar' in request.POST:
        cliente_seleccionado.is_active = False
        cliente_seleccionado.save()
        return HttpResponseRedirect('/listar_clientes/')
    elif request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_clientes/')
    else:
        return render_to_response('Gestion_de_clientes/eliminar_cliente.html',
            {'cliente': cliente_seleccionado,
                'usuario_sesion': usuario_sesion}, RequestContext(request))
