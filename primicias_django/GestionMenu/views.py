from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from tutorial.GestionPlatos.models import comida, postre
from forms import Tipos_Menu_form
from models import menu
from django.db.models import Q
# Create your views here.


#@login_required(login_url="/login/")
def crear_menu_view(request):
    comidas = []
    postres = []
    for e in comida.objects.all().order_by('nombre'):
        opt = [int(e.id), str(e.nombre)]
        comidas.append(opt)

    for e in postre.objects.all().order_by('nombre'):
        opt = [int(e.id), str(e.nombre)]
        postres.append(opt)
    if request.method == 'POST' and 'Guardar' in request.POST:
        fecha_seleccionada = request.POST.get('fecha')
        comidas_seleccionadas = request.POST.getlist('lista_comida[]')
        postres_seleccionados = request.POST.getlist('lista_postre[]')
        print('Comidas: ', comidas_seleccionadas)
        print('Postres: ', postres_seleccionados)
        print('Fecha: ', fecha_seleccionada)
        nuevo_menu = menu(fecha=fecha_seleccionada)
        nuevo_menu.save()
        for id_comida in comidas_seleccionadas:
            nuevo_menu.comida.add(comida.objects.get(pk=id_comida))
        for id_postre in postres_seleccionados:
            nuevo_menu.postre.add(postre.objects.get(pk=id_postre))
        return HttpResponseRedirect('/listar_menu/')
    return render_to_response("Gestion_de_menu/crear_menu.html",
        {'comidas': comidas, 'postres': postres},
        context_instance=RequestContext(request))


#@login_required(login_url="/login/")
def listar_menu_view(request):
    if request.method == 'POST':
        form = Tipos_Menu_form(request.POST)
        if form.is_valid():
            busqueda = form.cleaned_data.get('Busqueda')
            #Si el usuario ingresa "Todos"
            if busqueda == 'todos' or busqueda == 'Todos':
                comidas = comida.objects.all()
                context = {'form': form, 'comidas': comidas}
            #Si el usuario ingresa un tipo y un nombre especificos
            elif busqueda != '':
                comidas = \
                comida.objects.filter(
                    Q(nombre__icontains=busqueda)).order_by('nombre')
                context = {'form': form, 'comidas': comidas}
            else:
                form = Tipos_Menu_form()
                #tipos = "Ninguno" Es cuando el usuario oprime el boton buscar
                #sin ningun parametro de busqueda
                context = {'form': form}
        else:
            form = Tipos_Menu_form()
            #tipos = "No valido" Es cuando el parametro de busqueda es invalido
            context = {'form': form}

    else:
        form = Tipos_Menu_form()
        menus = menu.objects.filter(is_active='True').order_by('fecha')
        context = {'form': form, 'menus': menus}
    return render(request, 'Gestion_de_menu/listar_menu.html',
        context)



#@login_required(login_url="/login/")
def modificar_menu_view(request):
    pass


#@login_required(login_url="/login/")
def consultar_menu_view(request):
    pass


#@login_required(login_url="/login/")
def eliminar_menu_view(request):
    pass