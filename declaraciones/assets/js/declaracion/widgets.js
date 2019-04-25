module.exports.checkBoxText=function(name,other,active){
        if(active){
            $("#"+other).prop("readonly",false);
            $("#"+other).prop("required",true);
            $("#"+other).focus();
        }else{
            $("#"+other).prop("readonly",true);
            $("#"+other).prop("required",false);
            $("#"+other).val("");
        }
};
module.exports.checkBoxText2=function(name,other,active,other2){
        if(active){
            $("#"+other).prop("readonly",false);
            $("#"+other).prop("required",true);
            $("#"+other).focus();
        }else{
            $("#"+other).prop("readonly",true);
            $("#"+other).prop("required",false);
            $("#"+other).val("");
        }
        $("#"+other2).val("")
        $("#"+other2).prop("readonly",true);
};

module.exports.radioMx=function(v,id){

  if(v==='mx'){
      $("#"+id).val(142)
      $("#"+id+"_container").hide()
  } else{
      $("#"+id+"_container").show()
  }
};

module.exports.radioUnica=function(id){
  if(id=='id-frecuencia-container'){
      $("#id-frecuencia-container").show()
      $("#id-unica-container").hide()
  } else{
      $("#id-frecuencia-container").hide()
      $("#id-unica-container").show()
  }
};

module.exports.radioTPersona=function(v,id){

  if(v=='true'){
      $("#id_"+id+"_container_fisica").show()
      $("#id_"+id+"_container_moral").hide()

  } else{
      $("#id_"+id+"_container_fisica").hide()
      $("#id_"+id+"_container_moral").show()
  }
};

module.exports.borrarRegistro=function(url, redirect, id) {
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  function csrfSafeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });

  if (confirm('¿Está seguro de eliminar el registro?') == true) {
      $.ajax({
          url : url,
          type : "POST",
          success : function(json) {
            $("#borrar-registro-" + id).hide()
          },
          error : function(xhr,errmsg,err) {
              console.log(xhr.status + ": " + xhr.responseText);
          }
      });
  } else {
      return false;
  }
};


module.exports.borraUsuario=function(url,form,reload){
  var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
  function csrfSafeMethod(method) {
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
      $.ajax({
          url : url.replace('0',$("#id-usuario").val()),
          type : "POST",
          data:$("#"+form).serialize(),
          success : function(json) {
              if(reload===true) {
                  $("#id-usuario-" + $("#id-usuario").val()).remove();
                  $("#id-usuario").val("")
                  $("#nombre-usuario").html("")
                  $("#modal").modal('hide');
              } else{
                  window.location.href =reload;
              }
          },
          error : function(xhr,errmsg,err) {

          }
      });

};