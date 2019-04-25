$(document).ready(function() {
  $('#no_aplica').change(function() {
      if(this.checked) {
          $(".row-form").hide()
      }
      else {
        $(".row-form").show()
      }
  });
});
