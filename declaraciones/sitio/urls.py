from django.conf.urls import url
from django.urls import path, reverse_lazy, re_path

from sitio.views import LoginView, LogoutView, CambioPasswordView, PasswordResetRFCView,activar
from .views import (IndexView, FAQsView, InformacionView,
                    DeclaracionesPreviasView,
                    DeclaracionesPreviasDescargarView)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('preguntas-frecuentes', FAQsView.as_view(), name="preguntas-frecuentes"),
    path('informacion', InformacionView.as_view(), name="informacion"),
    path('declaraciones-previas', DeclaracionesPreviasView.as_view(), name="declaraciones-previas"),
    re_path(r'^declaraciones-previas/descargar/(?P<folio>[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12})/$',
            DeclaracionesPreviasDescargarView.as_view(),
            name="declaraciones-previas-descargar"),
    path('login', LoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('recuperar', LogoutView.as_view(), name="recuperar"),
    path('cambiar', CambioPasswordView.as_view(), name="cambiar"),
    path('password_reset/', PasswordResetRFCView.as_view(success_url=reverse_lazy('password_reset_done')),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    url(r'^activar/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activar, name='activar')
]
