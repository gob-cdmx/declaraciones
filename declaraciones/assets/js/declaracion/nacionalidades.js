$(document).ready(function() {
    $('.multiples-nacionalidades select').select2({
      placeholder: "Selecciona una o varias",
    });
    $('.agregar-nacionalidad').click(function() {
      $('.multiples-nacionalidades select').select2('open');
    })
});
