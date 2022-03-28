# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User


@login_required(login_url="/login/")
def main_view(request):
    """
    Redirecciona a la pagina principal al usuario, es necesario estar logueado
    """
    #usuario = funcionario.objects.get(id=request.user.id)
    usuario = usuario_main(request)
    print(('Usuario es: ', usuario))
    return render_to_response("Sistema/main.html", {'usuario_sesion': usuario},
        context_instance=RequestContext(request))


def login_view(request):
    """
    Redirecciona a la interfaz de logueo y obtiene los parametros del usuario
    para verificar.
    """
    username = password = ''
    status = "valido"
    if request.POST and 'Entrar' in request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/main/')
            else:
                status = "no activo"
                return render_to_response('Sistema/login.html',
                    {'username': username, 'status': status},
                    _instance=RequestContext(request))
        else:
            status = "invalido"
            return render_to_response('Sistema/login.html',
                {'username': username, 'status': status},
                context_instance=RequestContext(request),)
    return render_to_response('Sistema/login.html',
        {'username': username, 'status': status},
        context_instance=RequestContext(request))


def logout_view(request):
    """
    Redirecciona al usuario a la interfaz de logueo cerrando la sesion
    :param request:
    :return:
    """
    logout(request)
    return render_to_response("Sistema/login.html", locals(),
        context_instance=RequestContext(request))


def usuario_main(request):
    clave_sesion = request.session.session_key
    sesion = Session.objects.get(session_key=clave_sesion)
    id_usuario = sesion.get_decoded().get('_auth_user_id')
    return User.objects.get(pk=id_usuario)
