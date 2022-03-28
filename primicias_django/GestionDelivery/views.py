from django.shortcuts import render_to_response
from django.db.models import Q
from tutorial.GestionClientes.models import cliente
from tutorial.GestionUsuarios.models import funcionario
#from tutorial.GestionPlatos.models import postre
#from .forms import Tipos_Pedido_form
from tutorial.GestionPedidos.models import detalle_pedido, factura
from .models import zona, pedidoXzona
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from django.contrib.auth.models import User
import itertools
from io import BytesIO
#from django.core.exceptions import ObjectDoesNotExist
from tutorial.GestionSistema.views import usuario_main
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="/login/")
def crear_zona_view(request):
    encargados = User.objects.filter(groups__name='Delivery').filter(
        is_active='True').order_by('first_name')
    usuario_sesion = usuario_main(request)
    if request.method == 'POST' and 'Guardar' in request.POST:
        nombre = request.POST.get('nombre')
        encargado = funcionario.objects.get(pk=request.POST.get(
            'encargado'))
        nuevo = zona(nombre=nombre, encargado=encargado)
        print(('Encargado: ', encargado.id))
        nuevo.save()
        return HttpResponseRedirect('/listar_zonas/')
    return render_to_response("Gestion_de_delivery/crear_zona.html",
        {'encargados': encargados, 'usuario_sesion': usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def listar_zonas_view(request):
    zonas = zona.objects.filter(is_active=True)
    usuario_sesion = usuario_main(request)
    return render_to_response("Gestion_de_delivery/listar_zonas.html",
        {'zonas': zonas, 'usuario_sesion': usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def modificar_zona_view(request, id_zona):
    zona_seleccionada = zona.objects.get(pk=id_zona)
    usuario_sesion = usuario_main(request)
    encargados = User.objects.filter(groups__name='Delivery').filter(
        is_active='True').order_by('first_name')
    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_zonas/')
    if request.method == 'POST' and 'Guardar' in request.POST:
        zona_seleccionada.nombre = request.POST.get('nombre')
        zona_seleccionada.encargado = funcionario.objects.get(
            pk=request.POST.get('encargado'))
        zona_seleccionada.save()
        return HttpResponseRedirect('/listar_zonas/')
    return render_to_response("Gestion_de_delivery/modificar_zona.html",
        {'zona': zona_seleccionada, 'encargados': encargados,
            'usuario_sesion': usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def consultar_zona_view(request, id_zona):
    usuario_sesion = usuario_main(request)
    zona_seleccionada = zona.objects.get(pk=id_zona)
    if request.method == 'POST' and 'Retroceder' in request.POST:
        return HttpResponseRedirect('/listar_zonas/')
    return render_to_response("Gestion_de_delivery/consultar_zona.html",
        {'zona': zona_seleccionada, 'usuario_sesion': usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def eliminar_zona_view(request, id_zona):
    usuario_sesion = usuario_main(request)
    zona_seleccionada = zona.objects.get(pk=id_zona)
    if request.method == 'POST' and 'Cancelar' in request.POST:
        return HttpResponseRedirect('/listar_zonas/')
    if request.method == 'POST' and 'Aceptar' in request.POST:
        zona_seleccionada.is_active = False
        zona_seleccionada.save()
        return HttpResponseRedirect('/listar_zonas/')
    return render_to_response("Gestion_de_delivery/eliminar_zona.html",
        {'nombre': zona_seleccionada.nombre, 'usuario_sesion': usuario_sesion},
        context_instance=RequestContext(request))


@login_required(login_url="/login/")
def imprimir_delivery_view(request):
    usuario_sesion = usuario_main(request)
    zonas = zona.objects.filter(is_active=True)
    repartidores = User.objects.filter(groups__name='Delivery').filter(
        is_active='True').order_by('first_name')
    if 'Imprimir' in request.POST and request.method == 'POST':
        buff = BytesIO()
        costo = '0'
        fecha_seleccionada = datetime.strptime(str(request.POST.get('fecha')),
            "%d/%m/%Y")
        filename = fecha_seleccionada.strftime("%d_%m_%Y") + '.pdf'
        zona_seleccionada = zona.objects.get(pk=request.POST.get('zona'))
        cambiar_repartidor = request.POST.get('cambiar_repartidor')
        repartidor_seleccionado = User.objects.get(
            pk=zona_seleccionada.encargado.id)
        if cambiar_repartidor:
            print(('Repartidor: ', request.POST.get('encargado')))
            repartidor_seleccionado = User.objects.get(
                pk=request.POST.get('encargado'))
        filename = filename + '_' + repartidor_seleccionado.first_name + '.pdf'
        detalles_pedido = detalle_pedido.objects.filter(
            fecha=fecha_seleccionada).filter(
                zona=str(zona_seleccionada.id)).order_by('direccion')
        print(('Detalles pedido: ', detalles_pedido))
        facturas = factura.objects.filter(
            fecha_pago=fecha_seleccionada).filter(
                zona=str(zona_seleccionada.id)).filter(
                ~Q(cod_det_pedido='0')).order_by('direccion')

        doc = SimpleDocTemplate(buff, pagesize=A4,
            rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        doc.pagesize = portrait(A4)
        elements = []
        data = [
            ["Nombre", "Direccion", "Telefono", "Comida", "Cantidad", "Postre",
                "Cantidad", "Costo", "Factura"],
            ]
        if detalles_pedido:
            for factu, detalle in itertools.izip_longest(
                facturas, detalles_pedido):
                if factu and detalle:
                    if factu.cliente.id == detalle.cod_pedido.cliente.id:
                        cliente_detalle = cliente.objects.get(
                            pk=detalle.cod_pedido.cliente.id)
                        if detalle.comida == 'L':
                            comida = 'Verde'
                        elif detalle.comida == 'R':
                            comida = 'Naranja'
                        elif detalle.comida == 'S':
                            comida = 'Lila'
                        if detalle.cod_pedido.tipo_pago == 'D':
                            costo = detalle.costo
                        elif detalle.cod_pedido.tipo_pago == 'S' and\
                        detalle.cod_pedido.fecha_pago == datetime.today():
                            costo = detalle.cod_pedido.costo_pedido
                        if detalle.cod_pedido.factura:
                            factura_delivery = 'X'
                        else:
                            factura_delivery = ''
                        data.append([cliente_detalle.nombre, detalle.direccion,
                            detalle.telefono, comida,
                            str(detalle.cantidad_comida),
                            detalle.postre.nombre, str(detalle.cantidad_postre),
                            costo, factura_delivery])
                        nuevo_pedido_x_zona = pedidoXzona(
                            fecha_delivery=fecha_seleccionada,
                            zona=zona_seleccionada,
                            delivery=funcionario.objects.get(
                                pk=repartidor_seleccionado.id),
                            pedido=detalle_pedido.objects.get(pk=detalle.id))
                        try:
                            if factu.id:
                                nuevo_pedido_x_zona.factura =\
                                factura.objects.get(pk=factu.id)
                        except AttributeError:
                            pass
                        nuevo_pedido_x_zona.save()
                    else:
                        cliente_detalle = cliente.objects.get(
                            pk=detalle.cod_pedido.cliente.id)
                        costo = '0'
                        factura_delivery = ''
                        if detalle.comida == 'L':
                            comida = 'Verde'
                        elif detalle.comida == 'R':
                            comida = 'Naranja'
                        elif detalle.comida == 'S':
                            comida = 'Lila'
                        data.append([cliente_detalle.nombre, detalle.direccion,
                            detalle.telefono,
                            comida, str(detalle.cantidad_comida),
                            detalle.postre.nombre, str(detalle.cantidad_postre),
                            costo, factura_delivery])
                        nuevo_pedido_x_zona = pedidoXzona(
                            fecha_delivery=fecha_seleccionada,
                            zona=zona_seleccionada,
                            delivery=funcionario.objects.get(
                                pk=repartidor_seleccionado.id),
                            pedido=detalle_pedido.objects.get(pk=detalle.id))
                        try:
                            if factu.id:
                                nuevo_pedido_x_zona.factura =\
                                factura.objects.get(pk=factu.id)
                        except AttributeError:
                            pass
                        nuevo_pedido_x_zona.save()

                elif not factu and detalle:
                    cliente_detalle = cliente.objects.get(
                        pk=detalle.cod_pedido.cliente.id)
                    if detalle.comida == 'L':
                        comida = 'Verde'
                    elif detalle.comida == 'R':
                        comida = 'Naranja'
                    elif detalle.comida == 'S':
                        comida = 'Lila'
                    costo = '0'
                    factura_delivery = ''
                    data.append([cliente_detalle.nombre, detalle.direccion,
                        detalle.telefono, comida, str(detalle.cantidad_comida),
                        detalle.postre.nombre, str(detalle.cantidad_postre),
                        costo, factura_delivery])
                    nuevo_pedido_x_zona = pedidoXzona(
                            fecha_delivery=fecha_seleccionada,
                            zona=zona_seleccionada,
                            delivery=funcionario.objects.get(
                                pk=repartidor_seleccionado.id),
                            pedido=detalle_pedido.objects.get(pk=detalle.id))
                    try:
                        if factu.id:
                            nuevo_pedido_x_zona.factura =\
                            factura.objects.get(pk=factu.id)
                    except AttributeError:
                        pass
                    nuevo_pedido_x_zona.save()
        if facturas:
            for factu, detalle in itertools.izip_longest(
                facturas, detalles_pedido):
                print(("facturas: ", facturas.values()))
                print(("detalles_pedido: ", detalles_pedido.values()))
                print(("factu: ", factu))
                #print(('Factura cobrar: ', factu.cliente.id))
                #print(('Detalle: ', detalle.cod_pedido.cliente.id))
                if factu:
                    if factu.cliente.id != detalle.cod_pedido.cliente.id:
                        detalle_factura = detalle_pedido.objects.get(
                            pk=factu.cod_det_pedido)
                        if detalle_factura.cod_pedido.tipo_pago == 'D':
                            costo = detalle_factura.costo
                        elif detalle_factura.cod_pedido.tipo_pago == 'S' and\
                        detalle_factura.cod_pedido.fecha_pago == datetime.today():
                            costo = detalle_factura.cod_pedido.costo_pedido
                        if detalle_factura.cod_pedido.factura:
                            factura_delivery = 'X'
                        else:
                            factura_delivery = ''
                        data.append([factu.cliente.nombre, factu.direccion,
                            factu.telefono, 'COBRAR', '--', 'COBRAR', '--', costo,
                            factura_delivery])
                        nuevo_pedido_x_zona = pedidoXzona(
                                fecha_delivery=fecha_seleccionada,
                                zona=zona_seleccionada,
                                delivery=funcionario.objects.get(
                                    pk=repartidor_seleccionado.id),
                                factura=factura.objects.get(pk=factu.id))
                        try:
                            if detalle.id:
                                nuevo_pedido_x_zona.pedido =\
                                detalle_pedido.objects.get(pk=detalle.id)
                        except AttributeError:
                            pass
                        nuevo_pedido_x_zona.save()
        style = TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.green),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lavender),
            ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.90, colors.black),
            ])
        s = getSampleStyleSheet()
        s = s["BodyText"]
        estilo2 = ParagraphStyle(
            'default',
            fontName='Times-Roman',
            fontSize=10,
            leading=10,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            alignment=TA_CENTER,
            spaceBefore=0,
            spaceAfter=0,
            bulletFontName='Times-Roman',
            bulletFontSize=10,
            bulletIndent=0,
            textColor=colors.black,
            backColor=None,
            wordWrap=None,
            borderWidth=0,
            borderPadding=0,
            borderColor=None,
            borderRadius=None,
            allowWidows=1,
            allowOrphans=0,
            textTransform=None,  # 'uppercase' | 'lowercase' | None
            endDots=None,
            splitLongWords=1,
            )
        s.wordWrap = 'CJK'
        data2 = [[Paragraph(cell, estilo2) for cell in row] for row in data]
        t = Table(data2)
        t.setStyle(style)
        if not repartidor_seleccionado:
            titulo = zona_seleccionada.encargado.first_name + ' ' +\
            zona_seleccionada.encargado.first_name + '\n\n\n'
        else:
            titulo = repartidor_seleccionado.first_name + ' ' +\
            repartidor_seleccionado.last_name + '\n\n\n'
        estilo = getSampleStyleSheet()
        ptext = '<font size=22> Repartido por: </font>'
        elements.append(Paragraph(ptext, estilo["Title"]))
        ptext = '<font size=12>%s</font>' % titulo
        elements.append(Paragraph(ptext, estilo["Title"]))
        elements.append(t)
        doc.build(elements)
        response = HttpResponse(content_type='application/pdf')
        content_disposition = 'attachment; filename='
        content_disposition = content_disposition + filename
        response['Content-Disposition'] = content_disposition
        response.write(buff.getvalue())
        buff.close()
        return response

    return render_to_response("Gestion_de_delivery/imprimir_delivery.html",
        {'zonas': zonas, 'repartidores': repartidores,
            'usuario_sesion': usuario_sesion},
        context_instance=RequestContext(request))