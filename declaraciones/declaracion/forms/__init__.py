from .informacion_personal import (DeclaracionForm, InfoPersonalFijaForm,
                                   DomiciliosForm, InfoPersonalVarForm,
                                   ObservacionesForm, DatosCurricularesForm,
                                   DatosEncargoActualForm,
                                   ExperienciaLaboralForm,
                                   ConyugeDependientesForm)


from .intereses import (EmpresasSociedadesForm, MembresiasForm,
                        RepresentacionesActivasForm,
                        RepresentacionesPasivasForm,
                        SociosComercialesForm,
                        ClientesPrincipalesForm, OtrasPartesForm,
                        BeneficiosGratuitosForm, ApoyosForm)

from .pasivos import (DeudasForm, DeudasOtrosForm)

from .ingresos import (SueldosPublicosForm,IngresosVariosForm)

from .activos import (BienesMueblesForm, BienesInmueblesForm,
                      MueblesNoRegistrablesForm, InversionesForm,
                      EfectivoMetalesForm, FideicomisosForm,
                      BienesIntangiblesForm, CuentasPorCobrarForm,
                      BeneficiosEspecieForm, BienesPersonasForm,
                      ActivosBienesForm)

from .registro import (RegistroForm,CambioEntePublicoForm)
from .admin import (BusquedaDeclaranteForm)
from .admin import (BusquedaDeclaracionForm,BusquedaUsuariosForm,RegistroUsuarioForm)
from .confirmacion import ConfirmacionForm
