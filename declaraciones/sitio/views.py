import urllib
import uuid
# from django.core.files.storage import default_storage
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.generic import (TemplateView, FormView, RedirectView,
                                  ListView)
from django.views import View
from django.conf import settings
from django.utils.encoding import force_text
from sitio.util import account_activation_token
from sitio.forms import PasswordResetForm
from sitio.forms import LoginForm
from declaracion.models import (Declaraciones,
                                InfoPersonalVar,
                                InfoPersonalFija,
                                DatosCurriculares,
                                ExperienciaLaboral, Encargos,
                                ConyugeDependientes,
                                Secciones,
                                SeccionDeclaracion)
from easy_pdf.views import PDFTemplateView
from easy_pdf.rendering import render_to_pdf_response


class IndexView(TemplateView):
    template_name = "sitio/index.html"


class FAQsView(TemplateView):
    template_name = "sitio/faqs.html"


class InformacionView(TemplateView):
    template_name = "sitio/informacion.html"


class DeclaracionesPreviasView(ListView):
    template_name = "sitio/declaraciones-previas.html"
    context_object_name = "declaraciones"

    def get_queryset(self):
        queryset = Declaraciones.objects.filter(
            cat_estatus_id = 4,
            info_personal_fija__usuario=self.request.user
            )
        return queryset


class DeclaracionesPreviasDescargarView(PDFTemplateView):
    template_name = "sitio/descargar.html"
    download_filename = 'hello.pdf'

    def get(self, request, *args, **kwargs):
        usuario = request.user
        try:
            folio_declaracion = self.kwargs['folio']
            declaracion = Declaraciones.objects.filter(folio=uuid.UUID(folio_declaracion), info_personal_fija__usuario=request.user).first()
        except Exception as e:
            folio_declaracion = None

        if folio_declaracion:
            info_personal_var = InfoPersonalVar.objects.filter(declaraciones=declaracion).first()
            info_personal_fija = InfoPersonalFija.objects.filter(declaraciones=declaracion).first()
            datos_curriculares = DatosCurriculares.objects.filter(declaraciones=declaracion).first()
            encargos = Encargos.objects.filter(declaraciones=declaracion).first()
            experiecia_laboral = ExperienciaLaboral.objects.filter(declaraciones=declaracion).first()
            conyuge_dependientes = ConyugeDependientes.objects.filter(declaraciones=declaracion).first()
            activas = declaracion.representaciones_set.filter(es_representacion_activa=True).all()
            pasivas = declaracion.representaciones_set.filter(es_representacion_activa=False).all()

            sueldos = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=1).all()
            profesional = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=2).all()
            empresarial = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=3).all()
            menor = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=4).all()
            arrendamiento = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=5).all()
            intereses = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=6).all()
            premios = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=7).all()
            bienes = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=8).all()
            otros = declaracion.ingresosvarios_set.filter(cat_tipos_ingresos_varios_id=9).all()

            seccion = SeccionDeclaracion.objects.filter(
                declaraciones=declaracion,
                seccion__url='informacion-personal-observaciones'
                ).first()
            if seccion:
                observaciones_informacion_personal = seccion.observaciones
            else:
                observaciones_informacion_personal = ''

            seccion = SeccionDeclaracion.objects.filter(
                declaraciones=declaracion,
                seccion__url='intereses-observaciones'
                ).first()
            if seccion:
                observaciones_intereses = seccion.observaciones
            else:
                observaciones_intereses = ''

            seccion = SeccionDeclaracion.objects.filter(
                declaraciones=declaracion,
                seccion__url='ingresos-observaciones'
                ).first()
            if seccion:
                observaciones_ingreso = seccion.observaciones
            else:
                observaciones_ingreso = ''

            seccion = SeccionDeclaracion.objects.filter(
                declaraciones=declaracion,
                seccion__url='activos-observaciones'
                ).first()
            if seccion:
                observaciones_activos = seccion.observaciones
            else:
                observaciones_activos = ''

            seccion = SeccionDeclaracion.objects.filter(
                declaraciones=declaracion,
                seccion__url='pasivos-observaciones'
                ).first()
            if seccion:
                observaciones_pasivos = seccion.observaciones
            else:
                observaciones_pasivos = ''

            observaciones = ''

        else:
            declaracion = {}
            info_personal_var = {}
            info_personal_fija = {}
            datos_curriculares = {}
            encargos = {}
            experiecia_laboral = {}
            conyuge_dependientes = {}
            observaciones = ''

        data = {
            'declaracion': declaracion,
            'info_personal_var': info_personal_var,
            'info_personal_fija': info_personal_fija,
            'datos_curriculares': datos_curriculares,
            'encargos': encargos,
            'experiecia_laboral': experiecia_laboral,
            'conyuge_dependientes': conyuge_dependientes,
            'observaciones': observaciones,
            'folio_declaracion': folio_declaracion,
            'activas': activas,
            'pasivas': pasivas,
            'sueldos': sueldos,
            'profesional': profesional,
            'empresarial': empresarial,
            'menor': menor,
            'arrendamiento': arrendamiento,
            'intereses': intereses,
            'premios': premios,
            'bienes': bienes,
            'otros': otros,
            'observaciones_informacion_personal': observaciones_informacion_personal,
            'observaciones_intereses': observaciones_intereses,
            'observaciones_ingreso': observaciones_ingreso,
            'observaciones_activos': observaciones_activos,
            'observaciones_pasivos': observaciones_pasivos
        }

        # content = render_to_content_file(self.template_name, data)
        # file_name = u"{}.pdf".format(declaracion.folio)
        # default_storage.save(file_name, content)
        return render_to_pdf_response(request,self.template_name, data)


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "sitio/login.html"
    success_url =  reverse_lazy("declaracion:perfil")

    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(request, self.template_name, {'form': LoginForm()})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')

        try:
            user = User.objects.get(username=username)
            if user.password == '':
                url = reverse('password_reset')
                return HttpResponseRedirect(url + "?rfc=%s" % (username))
        except:
            pass

        form = LoginForm(request.POST)
        if form.is_valid():
            login(request,user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            return render(request,self.template_name,{'form':form})

        return super(LoginView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)


class LogoutView(RedirectView):
    pattern_name = 'login'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class PasswordResetRFCView(PasswordResetView):
    from_email=settings.EMAIL_SENDER
    form_class = PasswordResetForm
    def get(self,request,*args,**kwargs):
        rfc = request.GET.get('rfc')

        try:

            obj = User.objects.get(username=rfc,password='')
            form = PasswordResetForm(initial={'rfc':obj.username})
            return render(request,self.template_name,{'form':form})
        except Exception as e:

            #return HttpResponse(content_type="", status=500)
            return render(request, self.template_name, {'form': PasswordResetForm()})
            #return super(PasswordResetRFCView,self).get(request, *args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        if form.save(**opts):

            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponse(content="",status=500)


class CambioPasswordView(View):
    template_name = 'sitio/cambio-password.html'

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user)

        return render(request, self.template_name, {
            'form': form
        })

    @method_decorator(login_required(login_url='/login'))
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            if request.user.check_password(form.cleaned_data['new_password2']):
                messages.error(request,"Tu nueva contraseña es idéntica a la actual")
                return render(request, self.template_name, {
                    'form': form
                })

            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, '¡Tu contraseña a sido cambiada!')

            return redirect('declaracion:perfil')

        return render(request, self.template_name, {
                'form': form
        })

def activar(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, '¡Tu cuenta a sido activada. ¡Cambia tu contraseña!')
        return redirect('cambiar')
    else:
        return HttpResponse('¡El enlace es invalido!')
