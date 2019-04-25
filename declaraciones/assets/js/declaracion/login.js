$(function () {

    $("#recuperar").click(


        function (evt) {

            if($("#id_rfc_rs").val()!="") {
                $.ajax(
                    {
                        method: "POST",
                        url: "/password_reset/",
                        data: $("#form_reset").serialize()
                    }
                ).done(function (evt) {
                    $("#ventana-modal").modal('hide');
                    $(".modal-backdrop").hide(100);
                    $("#modal-recuperar-contrasena").modal('show');
                    $("#rec-rfc").find(".invalid-feedback").removeClass("is-invalid")
                    $("#rec-rfc").find(".invalid-feedback").remove()

                }).fail(function () {
                    if ($("#rec-rfc").find(".invalid-feedback").length == 0) {
                        $("#id_rfc_rs").addClass("is-invalid")
                        $("#rec-rfc").append("<div class=\"invalid-feedback\">RFC válido no registrado.</div>")
                    }
                })
            } else {
                $("#id_rfc_rs").focus()
            }
        }
    )

    $("#cambiar-ente").click(function(evt){
            $.ajax(
                {
                    method: "POST",
                    url: "/declaracion/registro/perfil",
                    data: $("#form_dependencia").serialize()
                }
            ).done(function (evt) {
                $("#ventana-modal").modal('hide');
                $(".modal-backdrop").hide(100);
                $("#modal-cambia-ente").modal('show');

            }).fail(function () {

            })

    })

})