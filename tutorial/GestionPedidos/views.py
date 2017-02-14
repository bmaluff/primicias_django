from django.shortcuts import render, render_to_response
from django.db.models import Q
from tutorial.GestionClientes.models import cliente
from tutorial.GestionPlatos.models import postre
from .forms import Tipos_Pedido_form
from .models import pedido, detalle_pedido, factura, pago
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from tutorial.GestionSistema.views import usuario_main
from django.views.decorators.csrf import csrf_exempt
#from time import strptime, strftime, mktime
#from django.core import serializers
#import json
# Create your views here.


@login_required(login_url="/login/")
def crear_pedido_view(request):
    """
    Redirecciona a la interfaz para la creacion de un usuario nuevo
    """
    #Primero creara un usuario de forma temporal para poder asignar los
    #permisos que sean elegidos
    usuario_sesion = usuario_main(request)
    if request.method == 'POST' and 'Guardar' in request.POST:
        id_cliente = request.POST.get('datos[id_cliente]')
        lista_direcciones = request.POST.getlist('direcciones[]')
        lista_telefonos = request.POST.getlist('telefonos[]')
        lista_postre = request.POST.getlist('postres[]')
        lista_cant_postre = request.POST.getlist('cantidad_postre[]')
        lista_comida = request.POST.getlist('comidas[]')
        lista_cant_comida = request.POST.getlist('cantidad_comida[]')
        lista_fecha = request.POST.getlist('fechas[]')
        quiere_factura = False
        id_pagador = request.POST.get('datos[id_pagador]')
        tipo_pago = request.POST.get('datos[tipo_pago]')
        costo = request.POST.get('datos[costo_total]').replace(".", "")
        if request.POST.get('datos[factura_input]'):
            quiere_factura = True

        fecha_pedido = datetime.today()
        pago_tercero = request.POST.get('datos[input_pago_tercero]')
        direccion_pago = request.POST.get('datos[direccion_pedido]')
        telefono_pago = request.POST.get('datos[telefono_pedido]')
        if id_cliente == '':
            print('Error id cliente')
            mensaje_error_cliente = '<div class="alert alert-danger '\
            'alert-dismissible "'\
            ' role="alert"><button type="button" class="close" data-dismiss='\
            '"alert" aria-label="Close"><span aria-hidden="true">&times;'\
            '</span></button><strong>Error!</strong> Seleccione un usuario!'\
            '</div>'
            return HttpResponse(mensaje_error_cliente, status=500)
        for fecha in lista_fecha:
            if fecha == '':
                mensaje_error_fecha = '<div class="alert alert-danger '\
                'alert-dismissible " role="alert"><button type="button" '\
                'class="close" data-dismiss="alert" aria-label="Close">'\
                '<span aria-hidden="true">&times;</span></button>'\
                '<strong>Error!</strong> Existe un pedido sin fecha de '\
                'Entrega!</div>'
                return HttpResponse(mensaje_error_fecha, status=500)
        if pago_tercero and id_pagador:
            cliente_pago = cliente.objects.get(pk=id_pagador)
        if not pago_tercero:
            cliente_pago = cliente.objects.get(pk=id_cliente)
        if pago_tercero and id_pagador == '':
            mensaje_error_pagador = '<div class="alert alert-danger '\
            'alert-dismissible " role="alert"><button type="button" '\
            'class="close" data-dismiss="alert" aria-label="Close">'\
            '<span aria-hidden="true">&times;</span></button>'\
            '<strong>Error!</strong> Seleccione un Pagador!</div>'
            return HttpResponse(mensaje_error_pagador, status=500)
        if tipo_pago == 'S':
            fecha_pago = datetime.strptime(str(
                request.POST.get('datos[fecha_pago]')), "%d/%m/%Y")
        elif tipo_pago == 'D' and len(lista_fecha) > 1:
            fecha_pago = ultima_fecha(lista_fecha)
        elif tipo_pago == 'D' and len(lista_fecha) == 1:
            fecha_pago = datetime.strptime(str(lista_fecha[0]), "%d/%m/%Y")
        #########
        cliente_pedido = cliente.objects.get(pk=id_cliente)
        nuevo_pedido = pedido(fecha_pedido=fecha_pedido,
            cliente=cliente_pedido, costo_pedido=costo,
            factura=quiere_factura, tipo_pago=tipo_pago, fecha_pago=fecha_pago)
        #if tipo_pago == 'S':
        #    nuevo_pedido.fecha_pago = fecha_pago
        #elif tipo_pago == 'D' and len(lista_fecha) > 1:
        #    nuevo_pedido.fecha_pago = ultima_fecha(lista_fecha)
        #elif tipo_pago == 'D' and len(lista_fecha) == 1:
        #    nuevo_pedido.fecha_pago = fecha_pedido
        print(('Pedido:  ', vars(nuevo_pedido).items()))
        nuevo_pedido.save()
        zona_pago = ''
        if direccion_pago == cliente_pago.direccion:
            zona_pago = cliente_pago.zona1
        else:
            zona_pago = cliente_pago.zona2
        nueva_factura = factura(cliente=cliente_pago,
            fecha_pago=fecha_pago, telefono=telefono_pago,
            direccion=direccion_pago, zona=zona_pago,
            cod_pedido=nuevo_pedido.id, cod_det_pedido=0)
        nueva_factura.save()
        for i, item in enumerate(lista_comida):
            zona_detalle = ''
            if lista_direcciones[i] == cliente_pedido.direccion:
                zona_detalle = cliente_pedido.zona1
            else:
                zona_detalle = cliente_pedido.zona2
            nuevo_detalle = detalle_pedido(
                cod_pedido=pedido.objects.get(pk=nuevo_pedido.id),
                comida=str(item),
                postre=postre.objects.get(pk=str(lista_postre[i])),
                cantidad_comida=str(lista_cant_comida[i]),
                cantidad_postre=str(lista_cant_postre[i]),
                costo=str(
                    int(
                        lista_cant_comida[i]
                        ) * 17000 + int(
                            lista_cant_postre[i]
                            ) * 4000),
                fecha=datetime.strptime(str(lista_fecha[i]), "%d/%m/%Y"),
                direccion=lista_direcciones[i],
                zona=zona_detalle,
                telefono=lista_telefonos[i]
                )
            print(('Detalles: ', vars(nuevo_detalle).items()))
            nuevo_detalle.save()
            zona_pago = ''
            if direccion_pago == cliente_pago.direccion:
                zona_pago = cliente_pago.zona1
            else:
                zona_pago = cliente_pago.zona2
            nueva_factura = factura(cliente=cliente_pago,
            fecha_pago=fecha_pago, direccion=direccion_pago,
            telefono=telefono_pago, zona=zona_pago,
            cod_pedido=nuevo_pedido.id, cod_det_pedido=nuevo_detalle.id)
            nueva_factura.save()
        for i in list(request.POST.items()):
            print(('I: ', i))
    TIPO_COMIDA = (
        ('L', 'Light'),
        ('R', 'Regular'),
        ('S', 'Saludable'),
        )
    postres = postre.objects.all()
    TIPO_PAGO = (
        ('D', 'Diario'),
        ('S', 'Semanal'),
        )
    return render_to_response("Gestion_de_pedidos/crear_pedido.html",
        {'opc_comida': TIPO_COMIDA, 'opc_postre': postres,
            'opc_pago': TIPO_PAGO, "usuario_sesion": usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def ajax_cliente_search_view(request):
    busqueda = request.POST.get('sugerencia')
    if busqueda is not None:
        cliente_posible = cliente.objects.filter(Q(nombre__icontains=busqueda) |
            Q(apellido__icontains=busqueda) |
            Q(telefono__icontains=busqueda) |
            Q(ruc_ci__icontains=busqueda) |
            Q(telefono_2__icontains=busqueda)).order_by('nombre')
    if request.method == 'POST':        
        print(('Texto: ', cliente_posible))
        return render_to_response("Gestion_de_pedidos/actualizar_clientes.html",
            {'cliente_posible': cliente_posible}, RequestContext(request))
    else:
        return render_to_response("Gestion_de_pedidos/actualizar_clientes.html",
            {'cliente_posible': cliente_posible}, RequestContext(request))


@login_required(login_url="/login/")
def listar_pedidos_view(request):
    usuario_sesion = usuario_main(request)
    if request.method == 'POST':
        form = Tipos_Pedido_form(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data.get('Busqueda')
            if '/' in busqueda:
                fecha_vieja = busqueda
                busqueda = formatear_fecha(fecha_vieja)
                #print((temporal))
            #Si el usuario ingresa "Todos"
            if busqueda == 'todos' or busqueda == 'Todos':
                pedidos = pedido.objects.filter(
                    is_active='True').order_by('fecha_pedido', 'id')
                context = {'form': form, 'pedidos': pedidos}
            #Si el usuario ingresa un tipo y un nombre especificos
            elif busqueda:
                pedidos = \
                pedido.objects.filter(Q(cliente__nombre__icontains=busqueda) |
                Q(cliente__apellido__icontains=busqueda) |
                Q(cliente__telefono__icontains=busqueda) |
                Q(cliente__telefono_2__icontains=busqueda) |
                Q(id__icontains=busqueda) |
                Q(fecha_pedido__icontains=busqueda)).order_by('fecha_pedido',
                'id')
                context = {'form': form, 'pedidos': pedidos}
            else:
                form = Tipos_Pedido_form()
                pedidos = pedido.objects.filter(
                    is_active='True').order_by('fecha_pedido', 'id')
                #tipos = "Ninguno" Es cuando el usuario oprime el boton buscar
                #sin ningun parametro de busqueda
                context = {'form': form, 'pedidos': pedidos}
        else:
            form = Tipos_Pedido_form()
            #tipos = "No valido" Es cuando el parametro de busqueda es invalido
            context = {'form': form}

    else:
        form = Tipos_Pedido_form()
        pedidos = pedido.objects.filter(
            is_active='True').order_by('fecha_pedido', 'id')
        #pedido_prueba = pedido.objects.get(pk=8)
        #print(('Pedido Prueba: ', vars(pedido_prueba).items()))

        context = {'form': form, 'pedidos': pedidos,
            "usuario_sesion": usuario_sesion}
    return render(request, 'Gestion_de_pedidos/listar_pedidos.html',
        context)


@login_required(login_url="/login/")
def modificar_pedido_view(request, id_pedido):
    """
    Redirecciona al usuario la modificacion de un usuario especifico
    :param id_usuario: el id del usuario que sera modificado
    :return:
    """
    usuario_sesion = usuario_main(request)
    #Se obtienen los datos del usuario
    pedido_seleccionado = pedido.objects.get(pk=id_pedido)
    detalles_pedido = detalle_pedido.objects.filter(cod_pedido__id=id_pedido)
    pagador_seleccionado = ''
    try:
        factura_seleccionada = factura.objects.get(
        cod_pedido=id_pedido, cod_det_pedido='0')
    except factura.DoesNotExist:
        factura_seleccionada = ''
    try:
        if factura_seleccionada.cliente.id != pedido_seleccionado.cliente.id:
            pagador_seleccionado = factura_seleccionada
    except AttributeError:
        pass
    TIPO_COMIDA = (
        ('L', 'Light'),
        ('R', 'Regular'),
        ('S', 'Saludable'),
        )
    postres = postre.objects.all()
    TIPO_PAGO = (
        ('D', 'Diario'),
        ('S', 'Semanal'),
        )

#    usuario_seleccionado = funcionario.objects.get(pk=id_usuario)

    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_pedidos/')

    if request.method == 'POST' and 'Guardar' in request.POST:
        id_cliente = request.POST.get('datos[id_cliente]')
        lista_direcciones = request.POST.getlist('direcciones[]')
        lista_telefonos = request.POST.getlist('telefonos[]')
        lista_postre = request.POST.getlist('postres[]')
        lista_cant_postre = request.POST.getlist('cantidad_postre[]')
        lista_comida = request.POST.getlist('comidas[]')
        lista_cant_comida = request.POST.getlist('cantidad_comida[]')
        lista_fecha = request.POST.getlist('fechas[]')
        quiere_factura = False
        lista_pago_detalle = request.POST.getlist('detalles_pagados[]')
        id_pagador = request.POST.get('datos[id_pagador]')
        tipo_pago = request.POST.get('datos[tipo_pago]')
        costo = request.POST.get('datos[costo_total]').replace(".", "")
        if request.POST.get('datos[factura_input]'):
            quiere_factura = True
        fecha_pedido = datetime.today()
        pago_tercero = request.POST.get('datos[input_pago_tercero]')
        direccion_pago = request.POST.get('datos[direccion_pedido]')
        telefono_pago = request.POST.get('datos[telefono_pedido]')
        if id_cliente == '':
            print('Error id cliente')
            mensaje_error_cliente = '<div class="alert alert-danger '\
            'alert-dismissible "'\
            ' role="alert"><button type="button" class="close" data-dismiss='\
            '"alert" aria-label="Close"><span aria-hidden="true">&times;'\
            '</span></button><strong>Error!</strong> Seleccione un usuario!'\
            '</div>'
            return HttpResponse(mensaje_error_cliente, status=500)
        for fecha in lista_fecha:
            if fecha == '':
                mensaje_error_fecha = '<div class="alert alert-danger '\
                'alert-dismissible " role="alert"><button type="button" '\
                'class="close" data-dismiss="alert" aria-label="Close">'\
                '<span aria-hidden="true">&times;</span></button>'\
                '<strong>Error!</strong> Existe un pedido sin fecha de '\
                'Entrega!</div>'
                return HttpResponse(mensaje_error_fecha, status=500)
        if pago_tercero and id_pagador:
            cliente_pago = cliente.objects.get(pk=id_pagador)
        if not pago_tercero:
            cliente_pago = cliente.objects.get(pk=id_cliente)
        if pago_tercero and id_pagador == '':
            mensaje_error_pagador = '<div class="alert alert-danger '\
            'alert-dismissible " role="alert"><button type="button" '\
            'class="close" data-dismiss="alert" aria-label="Close">'\
            '<span aria-hidden="true">&times;</span></button>'\
            '<strong>Error!</strong> Seleccione un Pagador!</div>'
            return HttpResponse(mensaje_error_pagador, status=500)
        if tipo_pago == 'S':
            fecha_pago = datetime.strptime(
                str(request.POST.get('datos[fecha_pago]')), "%d/%m/%Y")
        elif tipo_pago == 'D' and len(lista_fecha) > 1:
            fecha_pago = ultima_fecha(lista_fecha)
        elif tipo_pago == 'D' and len(lista_fecha) == 1:
            fecha_pago = fecha_pago = datetime.strptime(str(
                lista_fecha[0]), "%d/%m/%Y")
        #########
        cliente_pedido = cliente.objects.get(pk=id_cliente)
        pedido.objects.filter(pk=pedido_seleccionado.id).update(
            fecha_pedido=fecha_pedido,
            cliente=cliente_pedido, costo_pedido=costo,
            factura=quiere_factura, tipo_pago=tipo_pago, fecha_pago=fecha_pago)
        print(('Pedido:  ', vars(pedido_seleccionado).items()))
        zona_pago = ''
        if direccion_pago == cliente_pago.direccion:
            zona_pago = cliente_pago.zona1
        else:
            zona_pago = cliente_pago.zona2
        if factura_seleccionada == '':
            nueva_factura = factura(cliente=cliente_pago,
                fecha_pago=fecha_pago, direccion=direccion_pago,
                telefono=telefono_pago, zona=zona_pago,
                cod_pedido=pedido_seleccionado.id, cod_det_pedido=0)
            nueva_factura.save()
        else:
            factura.objects.filter(
                pk=factura_seleccionada.id).update(cliente=cliente_pago,
            fecha_pago=fecha_pago, direccion=direccion_pago,
            telefono=telefono_pago, zona=zona_pago,
            cod_pedido=pedido_seleccionado.id, cod_det_pedido=0)
            factura.objects.filter(
                cod_pedido=id_pedido).filter(~Q(cod_det_pedido='0')).delete()
        detalle_pedido.objects.filter(cod_pedido__id=id_pedido).delete()
        for i, item in enumerate(lista_comida):
            fecha_detalle = datetime.strptime(str(lista_fecha[i]), "%d/%m/%Y")
            zona_detalle = ''
            if lista_direcciones[i] == cliente_pedido.direccion:
                zona_detalle = cliente_pedido.zona1
            else:
                zona_detalle = cliente_pedido.zona2
            nuevo_detalle = detalle_pedido(
                cod_pedido=pedido.objects.get(pk=pedido_seleccionado.id),
                comida=str(item),
                postre=postre.objects.get(pk=str(lista_postre[i])),
                cantidad_comida=str(lista_cant_comida[i]),
                cantidad_postre=str(lista_cant_postre[i]),
                costo=str(
                    int(
                        lista_cant_comida[i]
                        ) * 17000 + int(
                            lista_cant_postre[i]
                            ) * 4000),
                fecha=fecha_detalle,
                direccion=lista_direcciones[i],
                zona=zona_detalle,
                telefono=lista_telefonos[i]
                )
            print(('Detalles: ', vars(nuevo_detalle).items()))
            nuevo_detalle.save()
            try:
                if lista_pago_detalle[i]:
                    pago_detalle = pago.objects.get(
                        cod_pedido__id=pedido_seleccionado.id,
                        fecha_pago=fecha_detalle
                        )
                    pago_detalle.update(cod_det_pedido=nuevo_detalle.id)
            except IndexError:
                print(('Son pedidos nuevos y no tienen estado de pago'))
            if tipo_pago == 'D' and len(lista_fecha) > 1:
                fecha_pago = fecha_detalle
            zona_pago = ''
            if direccion_pago == cliente_pago.direccion:
                zona_pago = cliente_pago.zona1
            else:
                zona_pago = cliente_pago.zona2
            nueva_factura = factura(cliente=cliente_pago,
            fecha_pago=fecha_pago, direccion=direccion_pago,
            telefono=telefono_pago, zona=zona_pago,
            cod_pedido=pedido_seleccionado.id,
            cod_det_pedido=nuevo_detalle.id
            )
            nueva_factura.save()
    """for indice, detalle in enumerate(detalles_pedido):
            print(('Indice: ', indice, ' detalle: ', detalle.comida))
            print(('Indice: ', indice, ' modificacion: ', lista_comida[indice]))
            detalle.update(
                cod_pedido=pedido.objects.get(pk=pedido_seleccionado.id),
                comida=str(lista_comida[indice]),
                postre=postre.objects.get(pk=str(lista_postre[indice])),
                cantidad_comida=str(lista_cant_comida[indice]),
                cantidad_postre=str(lista_cant_postre[indice]),
                costo=str(
                    int(
                        lista_cant_comida[indice]
                        ) * 17000 + int(
                            lista_cant_postre[indice]
                            ) * 4000),
                fecha=datetime.strptime(str(lista_fecha[indice]), "%d/%m/%Y"),
                direccion=lista_direcciones[indice]
                )
        print(('Indice fuera de for: ', indice))
        for detalle in lista_comida[indice+1:]:
            print(("Nueva comida: ", detalle))"""
    #for item in detalles_pedido:
    #    print((vars(item).items()))
    return render_to_response("Gestion_de_pedidos/modificar_pedido.html",
                              {"pedido": pedido_seleccionado,
                                  "detalles": detalles_pedido,
                                  "opc_comida": TIPO_COMIDA,
                                  "opc_postre": postres, "opc_pago": TIPO_PAGO,
                                  "pagador": pagador_seleccionado,
                                  "usuario_sesion": usuario_sesion},
                                      context_instance=RequestContext(request))


@login_required(login_url="/login/")
def consultar_pedido_view(request, id_pedido):
    usuario_sesion = usuario_main(request)
    pedido_seleccionado = pedido.objects.get(pk=id_pedido)
    detalles_pedido = detalle_pedido.objects.filter(cod_pedido__id=id_pedido)
    try:
        factura_seleccionada = factura.objects.get(
        cod_pedido=id_pedido, cod_det_pedido='0')
    except factura.DoesNotExist:
        factura_seleccionada = ''
    TIPO_COMIDA = (
        ('L', 'Light'),
        ('R', 'Regular'),
        ('S', 'Saludable'),
        )
    postres = postre.objects.all()
    TIPO_PAGO = (
        ('D', 'Diario'),
        ('S', 'Semanal'),
        )
    return render_to_response("Gestion_de_pedidos/consultar_pedido.html",
                              {"pedido": pedido_seleccionado,
                                  "detalles": detalles_pedido,
                                  "opc_comida": TIPO_COMIDA,
                                  "opc_postre": postres, "opc_pago": TIPO_PAGO,
                                  "pagador": factura_seleccionada,
                                  "usuario_sesion": usuario_sesion},
                                      context_instance=RequestContext(request))


@login_required(login_url="/login/")
def eliminar_pedido_view(request, id_pedido):
    usuario_sesion = usuario_main(request)
    pedido_seleccionado = pedido.objects.get(pk=id_pedido)
    if request.method == 'POST' and 'Aceptar' in request.POST:
        pedido_seleccionado.is_active = False
        pedido_seleccionado.save()
        return HttpResponseRedirect('/listar_pedidos/')
    elif request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_pedidos/')
    else:
        return render_to_response('Gestion_de_pedidos/eliminar_pedido.html',
            {'codigo': pedido_seleccionado.id,
                "usuario_sesion": usuario_sesion}, RequestContext(request))


def ultima_fecha(fechas=[]):
    mayor = datetime.strptime(str(fechas[0]), "%d/%m/%Y")
    print(('Mayor: ', mayor))
    for item in fechas:
        if datetime.strptime(str(item), "%d/%m/%Y") > mayor:
            mayor = datetime.strptime(str(item), "%d/%m/%Y")
    #return strftime("%d/%m/%Y", mayor)
    return mayor


def formatear_fecha(fecha_vieja):
    fecha_nueva = ''
    temporal = fecha_vieja.split('/')
    for indice, item in enumerate(reversed(temporal)):
        fecha_nueva += item
        if indice != (len(temporal) - 1):
            fecha_nueva += '-'
    return fecha_nueva
