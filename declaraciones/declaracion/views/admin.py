import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404

from declaracion.forms import BusquedaDeclaranteForm, BusquedaDeclaracionForm, BusquedaUsuariosForm,RegistroUsuarioForm
from declaracion.models import InfoPersonalFija, InfoPersonalVar, Declaraciones, DatosCurriculares, Encargos, \
    ConyugeDependientes, ExperienciaLaboral
from declaracion.views import RegistroView
from sitio.util import account_activation_token


class BusquedaDeclarantesFormView(View):
    template_name="declaracion/admin/busqueda-declarantes.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):

        if request.user.is_staff:
            return render(request,self.template_name,{'form':BusquedaDeclaranteForm()})
        else:
            return redirect('login')

    @method_decorator(login_required(login_url='/login'))
    def post(self,request,*args,**kwargs):
        if request.user.is_staff:
            form = BusquedaDeclaranteForm(request.POST )

            if form.is_valid():



                result = InfoPersonalFija.objects.filter(usuario__is_staff=False)
                page = form.cleaned_data.get('page')
                page_size =form.cleaned_data.get('page_size')
                nombre = form.cleaned_data.get('nombre')
                estatus = form.cleaned_data.get('estatus')


                if nombre and not nombre=="":
                    result = result.filter( nombres__icontains=nombre)
                apellido1 = form.cleaned_data.get('apellido1')
                if apellido1 and not apellido1=="":
                    result = result.filter( apellido1__icontains=apellido1)
                apellido2 = form.cleaned_data.get('apellido2')
                if apellido2 and not apellido2=="":
                    result = result.filter( apellido2__icontains=apellido2)
                rfc = form.cleaned_data.get('rfc')
                if rfc and not rfc=="":
                    result = result.filter( rfc__icontains=rfc)
                if estatus:
                    result = result.filter( declaraciones_set__cat_estatus = estatus )


                curp = form.cleaned_data.get('curp')
                if curp and not curp=="":
                    result = result.filter(curp__icontains=curp)
                if page and page.isdigit():
                    page = int(page)
                else:
                    page=1
                if page_size and page_size.isdigit():
                    page_size = int(page_size)
                else:
                    page_size=10


                paginator = Paginator(result, page_size)
                result = paginator.get_page(page)


            return render(request,self.template_name,{'form':BusquedaDeclaranteForm(),'result':result,'paginas': range(1, paginator.num_pages + 1)})
        else:
            return redirect('declaracion:index')

class BusquedaUsuariosFormView(View):
    template_name="declaracion/admin/busqueda-usuarios.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):

        if request.user.is_staff:
            return render(request,self.template_name,{'form':BusquedaUsuariosForm()})
        else:
            return redirect('login')

    @method_decorator(login_required(login_url='/login'))
    def post(self,request,*args,**kwargs):
        if request.user.is_staff:
            form = BusquedaUsuariosForm(request.POST )

            if form.is_valid():



                result = InfoPersonalFija.objects.filter(usuario__is_staff=True)
                page = form.cleaned_data.get('page')
                page_size =form.cleaned_data.get('page_size')
                nombre = form.cleaned_data.get('nombre')
                estatus = form.cleaned_data.get('estatus')


                if nombre and not nombre=="":
                    result = result.filter( nombres__icontains=nombre)
                apellido1 = form.cleaned_data.get('apellido1')
                if apellido1 and not apellido1=="":
                    result = result.filter( apellido1__icontains=apellido1)
                apellido2 = form.cleaned_data.get('apellido2')
                if apellido2 and not apellido2=="":
                    result = result.filter( apellido2__icontains=apellido2)
                if estatus:
                    result = result.filter( usuario__is_active = estatus )

                if page and page.isdigit():
                    page = int(page)
                else:
                    page=1
                if page_size and page_size.isdigit():
                    page_size = int(page_size)
                else:
                    page_size=10


                paginator = Paginator(result, page_size)
                result = paginator.get_page(page)


            return render(request,self.template_name,{'form':form,'result':result,'paginas': range(1, paginator.num_pages + 1)})
        else:
            return redirect('declaracion:index')


class BusquedaDeclaracionesFormView(View):
    template_name="declaracion/admin/busqueda-declaraciones.html"


    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):

        if request.user.is_staff:
            return render(request,self.template_name,{'form':BusquedaDeclaracionForm()})
        else:
            return redirect('login')

    @method_decorator(login_required(login_url='/login'))
    def post(self,request,*args,**kwargs):
        if request.user.is_staff:
            form = BusquedaDeclaracionForm(request.POST )

            if form.is_valid():



                result = Declaraciones.objects.all()
                page = form.cleaned_data.get('page')
                page_size =form.cleaned_data.get('page_size')
                folio = form.cleaned_data.get('folio')


                if folio and not folio=="":
                    result = result.filter(folio=uuid.UUID(folio))
                tipo = form.cleaned_data.get('tipo')
                if tipo :
                    result = result.filter( cat_tipos_declaracion=tipo)
                ente = form.cleaned_data.get('ente')
                if ente :
                    result = result.filter( encargos__cat_entes_publicos=ente )
                ano = form.cleaned_data.get('ano')
                if ano and not ano=="":
                    result = result.filter( fecha_declaracion__year=ano)
                estatus = form.cleaned_data.get('estatus')
                if estatus:
                    result = result.filter(cat_estatus=estatus)


                if page and page.isdigit():
                    page = int(page)
                else:
                    page=1
                if page_size and page_size.isdigit():
                    page_size = int(page_size)
                else:
                    page_size=10


                paginator = Paginator(result, page_size)
                result = paginator.get_page(page)


            return render(request,self.template_name,{'form':form,'result':result,'paginas': range(1, paginator.num_pages + 1)})
        else:
            return redirect('declaracion:index')



class InfoDeclarantesFormView(View):
    template_name="declaracion/admin/info-declarante.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):

        if request.user.is_staff:
            result = InfoPersonalFija.objects.get(pk=self.kwargs['pk'])
            declaraciones = result.declaraciones_set.all()

            info = InfoPersonalVar.objects.filter( declaraciones__in=declaraciones).first()


            return render(request,self.template_name,{'result':result,'info':info,'declaraciones':declaraciones})
        else:
            return redirect('login')


class InfoUsuarioFormView(View):
    template_name="declaracion/admin/info-usuario.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):

        if request.user.is_superuser:
            result = InfoPersonalFija.objects.get(usuario__pk=self.kwargs['pk'])
            return render(request,self.template_name,{'info':result})
        else:
            return redirect('login')



class InfoDeclaracionFormView(View):
    template_name="declaracion/admin/info-declaracion.html"

    @method_decorator(login_required(login_url='/login'))
    def get(self,request,*args,**kwargs):

        if request.user.is_staff:
            declaracion = Declaraciones.objects.get(pk=self.kwargs['pk'])
            info_personal_var = InfoPersonalVar.objects.filter(declaraciones=declaracion).first()
            info_personal_fija = InfoPersonalFija.objects.filter(declaraciones=declaracion).first()
            datos_curriculares = DatosCurriculares.objects.filter(declaraciones=declaracion).first()
            encargos_set = Encargos.objects.filter(declaraciones=declaracion).first()
            experiecia_laboral_set = ExperienciaLaboral.objects.filter(declaraciones=declaracion).first()
            conyuge_dependientes = ConyugeDependientes.objects.filter(declaraciones=declaracion).first()


            return render(request,self.template_name,{'declaracion':declaracion,
                                                      'info_personal_var':info_personal_var,
                                                      'info_personal_fija':info_personal_fija,
                                                      'datos_curriculares':datos_curriculares,
                                                      'encargos':encargos_set,
                                                      'experiecia_laboral':experiecia_laboral_set,
                                                      'conyuge_dependientes':conyuge_dependientes,
                                                      })
        else:
            return redirect('login')



class EliminarUsuarioFormView(View):

    @method_decorator(login_required(login_url='/login'))
    def post(self,request,*args,**kwargs):

        if request.user.is_superuser:
            user = User.objects.get(pk=self.kwargs['pk'])
            user.is_active=False
            user.save()
            return HttpResponse("",status=200)
        else:
            return HttpResponse("", status=500)




class NuevoUsuariosFormView(View):
    template_name = 'declaracion/admin/registro.html'
    template_redirect='declaracion/admin/busqueda-usuarios.html'
    form_redirect = BusquedaUsuariosForm
    is_staff = True
    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated or not request.user.is_superuser :
            raise Http404()

        return render(request, self.template_name, {
            'form': RegistroUsuarioForm(),
            'is_staff': self.is_staff
        })


    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser :
            raise Http404()

        registro = RegistroUsuarioForm(request.POST)

        if registro.is_valid():
            email = registro.cleaned_data.get('email')
            rfc = registro.cleaned_data.get('rfc')
            rfc = rfc.upper()


            password = User.objects.make_random_password()

            nombre = registro.cleaned_data.get("nombres")
            rol = registro.cleaned_data.get("rol")
            apellidos = registro.cleaned_data.get("apellido1")+" "+registro.cleaned_data.get("apellido2")

            user = User.objects.create_user(username=rfc,
                                            email=email,
                                            password=password,
                                            first_name=nombre,
                                            last_name=apellidos

                                            )
            user.is_superuser = registro.cleaned_data.get("rol")
            user.is_staff = True
            user.is_superuser=rol

            user.is_active=False

            user.save()

            datos = InfoPersonalFija(
                nombres=nombre,
                apellido1=registro.cleaned_data.get("apellido1"),
                apellido2=registro.cleaned_data.get("apellido2"),
                rfc=rfc,
                curp=registro.cleaned_data.get("rfc"),
                usuario=user,
                cat_ente_publico=registro.cleaned_data.get("dependencia"),
                telefono=registro.cleaned_data.get('telefono'),
                puesto=registro.cleaned_data.get('puesto')
            )
            datos.save()

            current_site = get_current_site(request)
            mail_subject = 'Activación de cuenta'
            message = render_to_string('declaracion/admin/acc_active_email_admin.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                'protocol': request.scheme,
                'password': password
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


        return render(request, self.template_name, {
            'form': registro,
            'is_staff':self.is_staff
        })


class EditarUsuarioFormView(View):
    template_name = 'declaracion/admin/registro.html'
    template_redirect='declaracion/admin/busqueda-usuarios.html'
    form_redirect = BusquedaUsuariosForm
    is_staff = True
    def get(self, request, *args, **kwargs):

        if request.user.is_authenticated and not self.is_staff:

            return redirect('logout')
        info = InfoPersonalFija.objects.get(usuario__pk=self.kwargs['pk'])
        print(info.usuario.email)
        initial = {
            'nombres':info.nombres,
            'apellido1':info.apellido1,
            'apellido2':info.apellido2,
            'dependencia':info.cat_ente_publico,
            'telefono':info.telefono,
            'rfc':info.rfc,
            'puesto':info.puesto,
            'email':info.usuario.email,
            'rol':info.usuario.is_superuser,
            'estatus':info.usuario.is_active,
            'id':info.usuario_id,
        }


        return render(request, self.template_name, {
            'form': RegistroUsuarioForm(initial=initial),
            'is_staff': self.is_staff,
            'editar':True,
            'info':info
        })


    def post(self, request, *args, **kwargs):
        registro = RegistroUsuarioForm(request.POST)

        if registro.is_valid():

            id = registro.cleaned_data.get('id')
            user = User.objects.get(pk=id)

            email = registro.cleaned_data.get('email')
            rfc = registro.cleaned_data.get('rfc')
            rfc = rfc.upper()
            nombre = registro.cleaned_data.get("nombres")
            apellidos = registro.cleaned_data.get("apellido1")+" "+registro.cleaned_data.get("apellido2")

            user.username=rfc
            user.email=email
            user.first_name=nombre
            user.last_name=apellidos

            user.is_superuser = registro.cleaned_data.get("rol")
            user.is_staff = True

            user.is_active=registro.cleaned_data.get("estatus")

            user.save()

            datos = InfoPersonalFija.objects.get(usuario__pk=id)

            datos.nombres=registro.cleaned_data.get("nombres")
            datos.apellido1=registro.cleaned_data.get("apellido1")
            datos.apellido2=registro.cleaned_data.get("apellido2")
            datos.rfc=rfc
            datos.curp=registro.cleaned_data.get("rfc")
            datos.cat_ente_publico=registro.cleaned_data.get("dependencia")
            datos.telefono=registro.cleaned_data.get('telefono')
            datos.puesto=registro.cleaned_data.get('puesto')
            datos.save()

            if self.form_redirect:
                return render(request,self.template_redirect,{'form':self.form_redirect(),'msg':False,'infopersonalfija':datos,'is_staff':self.is_staff,'editar':True})
            else:
                return render(request, self.template_redirect,
                              {'form': None, 'msg': False, 'infopersonalfija': datos,
                               'is_staff': self.is_staff,'editar':True})


        return render(request, self.template_name, {
            'form': registro,
            'is_staff':self.is_staff,
            'editar':True,

        })
