from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from .forms import Tipos_Comida_form, Tipos_Postre_form
from django.db.models import Q
from models import comida, postre
from django.contrib.auth.decorators import login_required
from tutorial.GestionSistema.views import usuario_main
# Create your views here.


@login_required(login_url="/login/")
def crear_comida_view(request):
    """
    Redirecciona a la interfaz para la creacion de un usuario nuevo
    """
    #Primero creara un usuario de forma temporal para poder asignar los
    #permisos que sean elegidos
    usuario_sesion = usuario_main(request)
    if request.method == 'POST' and 'Guardar' in request.POST:
        nombre = request.POST.get('nombre')
        calorias = request.POST.get('calorias')
        precio = request.POST.get('precio')

        if nombre != '' and calorias != '' and precio != '':
            # Se creara la comida
            nuevo = comida(nombre=nombre, calorias=calorias,
                precio=precio)
            print('Precio: ', precio)
            nuevo.save()

            return HttpResponseRedirect('/listar_comidas/')
        else:
            nuevo = comida(nombre=nombre, calorias=calorias,
                precio=precio)
            return render_to_response("Gestion_de_platos/crear_comida.html",
                {'error': 'vacio', 'comida': nuevo,
                    "usuario_sesion": usuario_sesion},
                context_instance=RequestContext(request))
    TIPO_COMIDA = (
        'Light',
        'Regular',
        'Saludable',
        )
    return render_to_response("Gestion_de_platos/crear_comida.html",
        {'opciones': TIPO_COMIDA, "usuario_sesion": usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def listar_comidas_view(request):
    """
    Permite al usuario realizar el listado de usuarios que se encuentran en el
    sistema habilitando con la opcion de filtrados de usuarios, tambien
    habilitara el boton para modificar, crear o eliminar si es que posee los
    permisos el usuario en sesion
    """
    usuario_sesion = usuario_main(request)
    if request.method == 'POST':
        form = Tipos_Comida_form(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data.get('Busqueda')
            #Si el usuario ingresa "Todos"
            if busqueda == 'todos' or busqueda == 'Todos':
                comidas = comida.objects.all()
                context = {'form': form, 'comidas': comidas,
                    "usuario_sesion": usuario_sesion}
            #Si el usuario ingresa un tipo y un nombre especificos
            elif busqueda != '':
                comidas = \
                comida.objects.filter(
                    Q(nombre__icontains=busqueda)).order_by('nombre')
                context = {'form': form, 'comidas': comidas,
                    "usuario_sesion": usuario_sesion}
            else:
                form = Tipos_Comida_form()
                #tipos = "Ninguno" Es cuando el usuario oprime el boton buscar
                #sin ningun parametro de busqueda
                context = {'form': form, "usuario_sesion": usuario_sesion}
        else:
            form = Tipos_Comida_form()
            #tipos = "No valido" Es cuando el parametro de busqueda es invalido
            context = {'form': form}

    else:
        form = Tipos_Comida_form()
        comidas = comida.objects.filter(is_active='True').order_by('nombre')

        context = {'form': form, 'comidas': comidas,
            "usuario_sesion": usuario_sesion}
    return render(request, 'Gestion_de_platos/listar_comidas.html',
        context)


@login_required(login_url="/login/")
def modificar_comida_view(request, id_comida):
    """
    Redirecciona al usuario la modificacion de un usuario especifico
    :param id_usuario: el id del usuario que sera modificado
    :return:
    """
    usuario_sesion = usuario_main(request)
    #Se obtienen los datos del usuario
    comida_seleccionada = comida.objects.get(pk=id_comida)
    TIPO_COMIDA = (
        'Light',
        'Regular',
        'Saludable',
        )
    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_comidas/')

    if request.method == 'POST' and 'Guardar' in request.POST:
        comida_seleccionada.nombre = request.POST.get('nombre')
        comida_seleccionada.calorias = request.POST.get('calorias')
        comida_seleccionada.precio = request.POST.get('precio')

            #Controla que no se hayan dejado en blanco ningun campo
        if comida_seleccionada.nombre != '' \
        and comida_seleccionada.calorias != '' \
        and comida_seleccionada.precio != '':

            comida_seleccionada.save()
            return HttpResponseRedirect('/listar_comidas/')
        else:
            return render_to_response(
                "Gestion_de_platos/modificar_comida.html",
                                      {'error': "vacio",
                                      'comida': comida_seleccionada,
                                      'opciones': TIPO_COMIDA,
                                      "usuario_sesion": usuario_sesion},
                                          context_instance=
                                          RequestContext(request))

    return render_to_response("Gestion_de_platos/modificar_comida.html",
                              {'comida': comida_seleccionada,
                                  'opciones': TIPO_COMIDA,
                                  "usuario_sesion": usuario_sesion},
                                      context_instance=RequestContext(request))


@login_required(login_url="/login/")
def consultar_comida_view(request, id_comida):
    usuario_sesion = usuario_main(request)
    comida_seleccionada = comida.objects.get(pk=id_comida)
    if request.method == 'POST' and 'Retroceder' in request.POST:
        return HttpResponseRedirect('/listar_comidas/')
    return render_to_response("Gestion_de_platos/consultar_comida.html",
        {"comida": comida_seleccionada, "usuario_sesion": usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def eliminar_comida_view(request, id_comida):
    """
    La funcion Eliminar en realidad solo cambia el estado del comida en
    la base de datos dejandolo inactivo, a fin de tener un registro sobre el
    historial de los comidas creados.
    """
    usuario_sesion = usuario_main(request)
    comida_seleccionada = comida.objects.get(pk=id_comida)
    if request.method == 'POST' and 'Aceptar' in request.POST:
        comida_seleccionada.is_active = False
        comida_seleccionada.save()
        return HttpResponseRedirect('/listar_comidas/')
    elif request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_comidas/')
    else:
        return render_to_response('Gestion_de_platos/eliminar_comida.html',
            {'nombre': comida_seleccionada.nombre,
                "usuario_sesion": usuario_sesion}, RequestContext(request))


@login_required(login_url="/login/")
def crear_postre_view(request):
    """
    Redirecciona a la interfaz para la creacion de un usuario nuevo
    """
    usuario_sesion = usuario_main(request)
    #Primero creara un usuario de forma temporal para poder asignar los
    #permisos que sean elegidos
    if request.method == 'POST' and 'Guardar' in request.POST:
        nombre = request.POST.get('nombre')
        calorias = request.POST.get('calorias')
        precio = request.POST.get('precio')

        if nombre != '' and calorias != '' and precio != '':
            # Se creara la postre
            nuevo = postre(nombre=nombre, calorias=calorias,
                precio=precio)
            nuevo.save()

            return HttpResponseRedirect('/listar_postres/')
        else:
            nuevo = postre(nombre=nombre, calorias=calorias,
                precio=precio)
            return render_to_response("Gestion_de_platos/crear_postre.html",
                {'error': 'vacio', 'postre': nuevo,
                    "usuario_sesion": usuario_sesion},
                context_instance=RequestContext(request))
    TIPO_COMIDA = (
        'Light',
        'Regular',
        'Saludable',
        )
    return render_to_response("Gestion_de_platos/crear_postre.html",
        {'opciones': TIPO_COMIDA, "usuario_sesion": usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def listar_postres_view(request):
    """
    Permite al usuario realizar el listado de usuarios que se encuentran en el
    sistema habilitando con la opcion de filtrados de usuarios, tambien
    habilitara el boton para modificar, crear o eliminar si es que posee los
    permisos el usuario en sesion
    """
    usuario_sesion = usuario_main(request)
    if request.method == 'POST':
        form = Tipos_Postre_form(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data.get('Busqueda')
            #Si el usuario ingresa "Todos"
            if busqueda == 'todos' or busqueda == 'Todos':
                postres = postre.objects.all()
                context = {'form': form, 'postres': postres,
                    "usuario_sesion": usuario_sesion}
            #Si el usuario ingresa un tipo y un nombre especificos
            elif busqueda != '':
                postres = \
                postre.objects.filter(
                    Q(nombre__icontains=busqueda)).order_by('nombre')
                context = {'form': form, 'postres': postres,
                    "usuario_sesion": usuario_sesion}
            else:
                form = Tipos_Postre_form()
                #tipos = "Ninguno" Es cuando el usuario oprime el boton buscar
                #sin ningun parametro de busqueda
                context = {'form': form,
                    "usuario_sesion": usuario_sesion}
        else:
            form = Tipos_Postre_form()
            #tipos = "No valido" Es cuando el parametro de busqueda es invalido
            context = {'form': form, "usuario_sesion": usuario_sesion}

    else:
        form = Tipos_Postre_form()
        postres = postre.objects.filter(is_active='True').order_by('nombre')

        context = {'form': form, 'postres': postres,
            "usuario_sesion": usuario_sesion}
    return render(request, 'Gestion_de_platos/listar_postres.html',
        context)


@login_required(login_url="/login/")
def modificar_postre_view(request, id_postre):
    """
    Redirecciona al usuario la modificacion de un usuario especifico
    :param id_usuario: el id del usuario que sera modificado
    :return:
    """
    usuario_sesion = usuario_main(request)
    #Se obtienen los datos del usuario
    postre_seleccionada = postre.objects.get(pk=id_postre)
    TIPO_COMIDA = (
        'Light',
        'Regular',
        'Saludable',
        )

    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_postres/')

    if request.method == 'POST' and 'Guardar' in request.POST:
        postre_seleccionada.nombre = request.POST.get('nombre')
        postre_seleccionada.calorias = request.POST.get('calorias')
        postre_seleccionada.precio = request.POST.get('precio')

            #Controla que no se hayan dejado en blanco ningun campo
        if postre_seleccionada.nombre != '' \
        and postre_seleccionada.calorias != '' \
        and postre_seleccionada.precio != '':

            postre_seleccionada.save()
            return HttpResponseRedirect('/listar_postres/')
        else:
            return render_to_response(
                "Gestion_de_platos/modificar_postre.html",
                                      {'error': "vacio",
                                      'postre': postre_seleccionada,
                                      'opciones': TIPO_COMIDA,
                                      "usuario_sesion": usuario_sesion},
                                          context_instance=
                                          RequestContext(request))

    return render_to_response("Gestion_de_platos/modificar_postre.html",
                              {'postre': postre_seleccionada,
                                  'opciones': TIPO_COMIDA,
                                  "usuario_sesion": usuario_sesion},
                                      context_instance=RequestContext(request))


@login_required(login_url="/login/")
def consultar_postre_view(request, id_postre):
    usuario_sesion = usuario_main(request)
    postre_seleccionada = postre.objects.get(pk=id_postre)
    if request.method == 'POST' and 'Retroceder' in request.POST:
        return HttpResponseRedirect('/listar_postres/')
    return render_to_response("Gestion_de_platos/consultar_postre.html",
        {"postre": postre_seleccionada,
            "usuario_sesion": usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def eliminar_postre_view(request, id_postre):
    """
    La funcion Eliminar en realidad solo cambia el estado del postre en
    la base de datos dejandolo inactivo, a fin de tener un registro sobre el
    historial de los postres creados.
    """
    usuario_sesion = usuario_main(request)
    postre_seleccionada = postre.objects.get(pk=id_postre)
    if request.method == 'POST' and 'Aceptar' in request.POST:
        postre_seleccionada.is_active = False
        postre_seleccionada.save()
        return HttpResponseRedirect('/listar_postres/')
    elif request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_postres/')
    else:
        return render_to_response('Gestion_de_platos/eliminar_postre.html',
            {'nombre': postre_seleccionada.nombre,
                "usuario_sesion": usuario_sesion}, RequestContext(request))