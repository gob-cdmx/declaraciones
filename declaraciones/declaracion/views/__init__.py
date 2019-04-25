from .informacion_personal import (DeclaracionFormView, DatosCurricularesView,
                                   DatosEncargoActualView,
                                   ExperienciaLaboralView,
                                   ConyugeDependientesView,
                                   InformacionPersonalObservacionesView,
                                   DatosCurricularesDelete,
                                   ExperienciaLaboralDeleteView,
                                   ConyugeDependientesDeleteView)

from .intereses import (EmpresasSociedadesView, MembresiaView,
                        RepresentacionesActivasView,
                        RepresentacionesPasivasView,
                        SociosComercialesView,
                        ClientesPrincipalesView, OtrasPartesFormView,
                        BeneficiosGratuitosView, ApoyosView,
                        InteresesObservacionesView,
                        EmpresasSociedadesDeleteView,
                        MembresiaDeleteView,
                        SociosComercialesDeleteView,
                        ClientesPrincipalesDeleteView,
                        OtrasPartesFormDeleteView,
                        BeneficiosGratuitosDeleteView,
                        ApoyosDeleteView,
                        RepresentacionesActivasDeleteView,
                        RepresentacionesPasivasDeleteView)

from .pasivos import (DeudasView, DeudasOtrosView, PasivosObservacionesView,
                      DeudasOtrosDeleteView, DeudasDeleteView)

from .ingresos import (SueldosPublicosView, IngresosVariosView,
                       IngresosObservacionesView, IngresosVariosDeleteView)

from .activos import (BienesMueblesView, BienesInmueblesView,
                      MueblesNoRegistrablesView, InversionesView,
                      EfectivoMetalesView, FideicomisosView,
                      BienesIntangiblesView, CuentasPorCobrarView,
                      BeneficiosEspecieView, ActivosObservacionesView,
                      BienesInmueblesDeleteView, BienesMueblesDeleteView,
                      MueblesNoRegistrablesDeleteView,
                      InversionesDeleteView,
                      EfectivoMetalesDeleteView,
                      FideicomisosDeleteView,
                      BienesIntangiblesDeleteView,
                      CuentasPorCobrarDeleteView,
                      BeneficiosEspecieDeleteView)

from .declaracion import (DeclaracionView, DeclaracionDeleteView)
from .registro import (RegistroView,PerfilView)
from .api import (RegistrosView)
from .confirmacion import (ConfimacionInformacionPersonalView,
                           ConfimacionInteresesView, ConfimacionPasivosView,
                           ConfimacionIngresosView, ConfimacionActivosView,
                           ConfirmarDeclaracionView)
from .admin import (BusquedaDeclarantesFormView,InfoDeclarantesFormView,InfoDeclaracionFormView,
                    BusquedaDeclaracionesFormView,BusquedaUsuariosFormView,NuevoUsuariosFormView,
                    EliminarUsuarioFormView,InfoUsuarioFormView,EditarUsuarioFormView)
