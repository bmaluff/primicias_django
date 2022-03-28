"""tutorial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from tutorial.GestionSistema import views as sistema_views
from tutorial.GestionDelivery import views as delivery_views
from tutorial.GestionMenu import views as menu_views
from tutorial.GestionPedidos import views as pedidos_views
from tutorial.GestionPlatos import views as platos_views
from tutorial.GestionRolesyPermisos import views as rol_views
from tutorial.GestionClientes import views as clientes_views
from tutorial.GestionUsuarios import views as usuarios_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', sistema_views.login_view,
        name='login'),
    url(r'^login', sistema_views.login_view, name='login'),
    url(r'^logout', sistema_views.logout_view, name='logout'),
    url(r'^main', sistema_views.main_view, name='main'),
    url(r'^crear_usuario', usuarios_views.crear_usuario_view,
        name='crear_usuario'),
    url(r'^listar_usuarios',
        usuarios_views.listar_usuarios_view, name='listar_usuarios'),
    url(r'^modificar_usuario/(?P<id_usuario>\d+)$',
        usuarios_views.modificar_usuario_view, name='modificar_usuario'),
    url(r'^consultar_usuario/(?P<id_usuario>\d+)$',
        usuarios_views.consultar_usuario_view, name='consultar_usuario'),
    url(r'^eliminar_usuario/(?P<id_usuario>\d+)$',
        usuarios_views.eliminar_usuario_view, name='eliminar_usuario'),
    url(r'^cambiar_password',
        usuarios_views.cambiar_password_view, name='cambiar_password'),
    url(r'^crear_rol', rol_views.crear_rol_view, name='crear_rol'),
    url(r'^listar_roles',
        rol_views.listar_roles_filtro_view, name='listar_roles'),
    url(r'^modificar_rol/(?P<id_rol>\d+)$',
        rol_views.modificar_rol_view, name='modificar_rol'),
    url(r'^consultar_rol/(?P<id_rol>\d+)$',
        rol_views.consultar_rol_view, name='consultar_rol'),
    url(r'^eliminar_rol/(?P<id_rol>\d+)$',
        rol_views.eliminar_rol_view, name='eliminar_rol'),
    url(r'^crear_cliente', clientes_views.crear_cliente_view,
        name='crear_cliente'),
    url(r'^listar_clientes',
        clientes_views.listar_clientes_view, name='listar_clientes'),
    url(r'^modificar_cliente/(?P<id_cliente>\d+)$',
        clientes_views.modificar_cliente_view, name='modificar_cliente'),
    url(r'^consultar_cliente/(?P<id_cliente>\d+)$',
        clientes_views.consultar_cliente_view, name='consultar_cliente'),
    url(r'^eliminar_cliente/(?P<id_cliente>\d+)$',
        clientes_views.eliminar_cliente_view, name='eliminar_cliente'),
    url(r'^crear_comida', platos_views.crear_comida_view,
        name='crear_comida'),
    url(r'^listar_comidas',
        platos_views.listar_comidas_view, name='listar_comidas'),
    url(r'^modificar_comida/(?P<id_comida>\d+)$',
        platos_views.modificar_comida_view, name='modificar_comida'),
    url(r'^consultar_comida/(?P<id_comida>\d+)$',
        platos_views.consultar_comida_view, name='consultar_comida'),
    url(r'^eliminar_comida/(?P<id_comida>\d+)$',
        platos_views.eliminar_comida_view, name='eliminar_comida'),
    url(r'^crear_postre', platos_views.crear_postre_view, name='crear_postre'),
    url(r'^listar_postres',
        platos_views.listar_postres_view, name='listar_postres'),
    url(r'^modificar_postre/(?P<id_postre>\d+)$',
        platos_views.modificar_postre_view, name='modificar_postre'),
    url(r'^consultar_postre/(?P<id_postre>\d+)$',
        platos_views.consultar_postre_view, name='consultar_postre'),
    url(r'^eliminar_postre/(?P<id_postre>\d+)$',
        platos_views.eliminar_postre_view, name='eliminar_postre'),
    url(r'^crear_menu', menu_views.crear_menu_view, name='crear_menu'),
    url(r'^listar_menu',
        menu_views.listar_menu_view, name='listar_menu'),
    url(r'^modificar_menu/(?P<id_menu>\d+)$',
        menu_views.modificar_menu_view, name='modificar_menu'),
    url(r'^consultar_menu/(?P<id_menu>\d+)$',
        menu_views.consultar_menu_view, name='consultar_menu'),
    url(r'^eliminar_menu/(?P<id_menu>\d+)$',
        menu_views.eliminar_menu_view, name='eliminar_menu'),
    url(r'^crear_pedido', pedidos_views.crear_pedido_view,
        name='crear_pedido'),
    url(r'^listar_pedidos',
        pedidos_views.listar_pedidos_view, name='listar_pedidos'),
    url(r'^modificar_pedido/(?P<id_pedido>\d+)$',
        pedidos_views.modificar_pedido_view, name='modificar_pedido'),
    url(r'^consultar_pedido/(?P<id_pedido>\d+)$',
        pedidos_views.consultar_pedido_view, name='consultar_pedido'),
    url(r'^eliminar_pedido/(?P<id_pedido>\d+)$',
        pedidos_views.eliminar_pedido_view, name='eliminar_pedido'),
    # url(r'^reporte_dia_pedidos',
    #    'tutorial.GestionPedidos.views.reporte_pedido_x_dia_view',
    #     name='reporte_pedido_dia'),
    url(r'^cliente_search',
        pedidos_views.ajax_cliente_search_view, name='cliente_search'),
    url(r'^crear_zona', delivery_views.crear_zona_view, name='crear_zona'),
    url(r'^listar_zonas',
        delivery_views.listar_zonas_view, name='listar_zonas'),
    url(r'^modificar_zona/(?P<id_zona>\d+)$',
        delivery_views.modificar_zona_view, name='modificar_zona'),
    url(r'^consultar_zona/(?P<id_zona>\d+)$',
        delivery_views.consultar_zona_view, name='consultar_zona'),
    url(r'^eliminar_zona/(?P<id_zona>\d+)$',
        delivery_views.eliminar_zona_view, name='eliminar_zona'),
    url(r'^imprimir_recorrido',
        delivery_views.imprimir_delivery_view, name='imprimir_recorrido'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
