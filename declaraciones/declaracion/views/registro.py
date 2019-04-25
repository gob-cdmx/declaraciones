from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View

from declaracion.forms import RegistroForm, CambioEntePublicoForm
from declaracion.models import InfoPersonalFija, InfoPersonalVar, Declaraciones
from declaracion.views.utils import obtiene_avance, obtiene_rfc
from sitio.util import account_activation_token
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q



class RegistroView(View):
    template_name = 'declaracion/registro.html'
    template_redirect='sitio/login.html'
    form_redirect = None
    is_staff = False
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated and not self.is_staff:

            return redirect('logout')

        return render(request, self.template_name, {
            'form': RegistroForm(),
            'is_staff': self.is_staff
        })


    def post(self, request, *args, **kwargs):
        registro = RegistroForm(request.POST)

        if registro.is_valid():
            email = registro.cleaned_data.get('email')
            rfc = registro.cleaned_data.get('rfc')
            rfc = rfc.upper()


            password = registro.cleaned_data.get('contrasena1')

            nombre = registro.cleaned_data.get("nombres")
            apellidos = registro.cleaned_data.get("apellido1")+" "+registro.cleaned_data.get("apellido2")

            user = User.objects.create_user(username=rfc,
                                            email=email,
                                            password=password,
                                            first_name=nombre,
                                            last_name=apellidos

                                            )
            user.is_active=False
            user.is_staff=self.is_staff
            user.save()

            ##TODO: Definir si el registro de los datos va a VAr o a FIJO
            datos = InfoPersonalFija(
                nombres=nombre,
                apellido1=registro.cleaned_data.get("apellido1"),
                apellido2=registro.cleaned_data.get("apellido2"),
                rfc=rfc,
                fecha_nacimiento = obtiene_rfc(rfc),
                cat_pais=registro.cleaned_data.get("pais"),
                cat_entidades_federativas =registro.cleaned_data.get("entidad"),
                curp=registro.cleaned_data.get("curp"),
                usuario=user,
                cat_ente_publico=registro.cleaned_data.get("dependencia"),
                fecha_inicio=registro.cleaned_data.get('fecha'),
                telefono=registro.cleaned_data.get('telefono'),
                puesto=registro.cleaned_data.get('puesto')
            )
            datos.save()





            #user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activación de cuenta'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                'protocol': request.scheme
            })
            to_email = email
            email = EmailMultiAlternatives(
                        mail_subject, message, to=[to_email],from_email=settings.EMAIL_SENDER
            )
            email.attach_alternative(message, "text/html")
            email.send()
            if self.form_redirect:
                return render(request,self.template_redirect,{'form':self.form_redirect(),'msg':True,'infopersonalfija':datos,'is_staff':self.is_staff})
            else:
                return render(request, self.template_redirect,
                              {'form': None, 'msg': True, 'infopersonalfija': datos,
                               'is_staff': self.is_staff})
            #return redirect('login')

        return render(request, self.template_name, {
            'form': registro,
            'is_staff':self.is_staff
        })

class PerfilView(View):
    template_name="declaracion/perfil.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:

            return redirect('login')

        form = CambioEntePublicoForm()
        infopersonalfija = InfoPersonalFija.objects.filter(usuario=request.user).first()
        if infopersonalfija is None:
            declaracion = None
        else:


            try:
                declaracion = Declaraciones.objects.filter(info_personal_fija=infopersonalfija).filter(
                    Q(cat_estatus__isnull=True) | Q(cat_estatus__pk__in=(1, 2, 3))).first()
            except:
                pass

            try:


                declaracion.avance= obtiene_avance(declaracion)[0]
                declaracion.save()
            except Exception as e:
                print(e)

        return render(request, self.template_name, {
            'user':request.user,
            'form':form,
            'infopersonalfija':infopersonalfija,
            'declaracion':declaracion
        })



    @method_decorator(login_required(login_url='/login'))
    def post(selfself,request):
        form = CambioEntePublicoForm(request.POST)
        if form.is_valid():
            InfoPersonalFija.objects.filter(usuario=request.user).update(cat_ente_publico=form.cleaned_data.get('dependencia'))
            return HttpResponse(content="",status=200)
        else:
            return HttpResponse(content="Campo sin llenar",status=500)
