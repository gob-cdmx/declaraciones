$(document).ready(function() {
  window.onscroll = function() {
    var position = document.body.clientHeight - window.scrollY - window.innerHeight
    if (position > 120) {
      $('.print-button').css({
        bottom: '20px',
      });
    } else {
      $('.print-button').css({
        bottom: (140 - position) + 'px',
      });
    }
  }

  $(".imprimir-pagina").click(function() {
    window.print()
  })
})
