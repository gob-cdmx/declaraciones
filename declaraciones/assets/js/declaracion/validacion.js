$(function () {

    $(".valida_email :input").keyup(function () {
        let re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        if (re.test($(this).val())) {
            $(this).removeClass("is-invalid")
            $(this).next().remove()
        }
        else {
            if ($(this).parent().find(".invalid-feedback").length == 0) {
                $(this).addClass("is-invalid")
                $(this).parent().append("<div class=\"invalid-feedback\">Introduzca una dirección de correo electrónico válida.</div>")
            }
        }
    });

    $(".valida_rfc :input").keyup(function () {

        let re = /^([A-Z,Ñ,&]{3,4}([0-9]{2})(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[A-Z|\d]{3})$/;

        $(this).val($(this).val().toUpperCase());


        if (re.test($(this).val())) {
            $(this).removeClass("is-invalid")
            $(this).next().remove()
        }
        else {
            if ($(this).parent().find(".invalid-feedback").length == 0) {
                $(this).addClass("is-invalid")
                $(this).parent().append("<div class=\"invalid-feedback\">Introduzca una RFC válido.</div>")
            }
        }
    });

    $(".valida_curp :input").keyup(function () {

        let re = /[A-Z]{1}[AEIOU]{1}[A-Z]{2}[0-9]{2}(0[1-9]|1[0-2])(0[1-9]|1[0-9]|2[0-9]|3[0-1])[HM]{1}(AS|BC|BS|CC|CS|CH|CL|CM|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]{1}[0-9]{1}$/;

        $(this).val($(this).val().toUpperCase());

        if (re.test($(this).val())) {
            $(this).removeClass("is-invalid")
            $(this).next().remove()
        }
        else if ($(this).parent().find(".invalid-feedback").length == 0) {
            $(this).addClass("is-invalid")
            $(this).parent().append("<div class=\"invalid-feedback\">Introduzca un CURP válido.</div>")
        }
    });
    $(".solo_letras :input").keyup(function () {
        this.value = this.value.replace(/[^a-zA-Z\s\u00f1\u00d1\u00E0-\u00FC\u00C0-\u00DC]/g, '').toUpperCase();
    });

    $(".solo_numeros :input").keyup(function () {
        this.value = this.value.replace(/[^0-9]/g, '');
    });

    $(".valida_telefono :input").keyup(function () {
        this.value = this.value.replace(/[^0-9]/g, '');
        max_length = 13;
        min_length = 8;
        $(this).attr("maxlength", max_length);

        if ($(this).val().length <= max_length && (this).val().length >= min_length) {
            $(this).removeClass("is-invalid")
        }
        else {
            $(this).addClass("is-invalid")
        }
    });
    $(".valida_cp :input").keyup(function () {
        this.value = this.value.replace(/[^0-9]/g, '');
        max_length = 5;

        $(this).attr("maxlength", max_length);

        if ($(this).val().length == max_length) {
            $(this).removeClass("is-invalid")
        }
        else {
            $(this).addClass("is-invalid")
        }
    });
    $(".valida_password :input").keyup(function () {
        max_length = 12;
        expresion_regular = "^[a-zA-Z0-9.!#$%&’*+/=?^_`{|}]{8,12}";

        $(this).val($(this).val().toUpperCase());
        $(this).attr("maxlength", max_length);

        if ($(this).val().match(expresion_regular) && $(this).val().length >= 8) {
            $(this).removeClass("is-invalid")
        }
        else {
            $(this).addClass("is-invalid")
        }
    });


    $(".entidad select").each(function(){
        let val = $(this).val();
        if( val==""|| val=="-1"||val==undefined){
            $(this).val(9);
        }
    });

    $(".pais select").each(function(){
        let val = $(this).val();
        if( val==""|| val=="-1"||val==undefined||val==142){
            $(this).val(142);
            $("#id-"+$(this).attr('name')+"-mx").click();
            $("#id_"+$(this).attr('name')+"_container").hide()
        } else {
             $("#id-"+$(this).attr('name')+"-ex").change();
        }
    });

    $(".moneda select").each(function(){
        let val = $(this).val();
        if( val==""|| val=="-1"||val==undefined||val==101){
            $(this).val(101);
            $("#id-"+$(this).attr('name')+"-mx").click();
            $("#id_"+$(this).attr('name')+"_container").hide()
        }
    });

    $(".tipo_persona :checked").change()


    $(".date :input").prop('readonly', true);
    $("#id_dependencia").selectize();
    $("#modal-aviso-declaracion-activa").modal('show',{
    		backdrop: 'static',
    		keyboard: false
		})
});
