from django.urls import path

from declaracion.views import (DeclaracionView)

urlpatterns = [
    path('', DeclaracionView.as_view(), name="declaracion"),
]
