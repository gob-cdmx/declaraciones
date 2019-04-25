$('.sidebar__link').each((i, e) => {
    let href = $(e).attr('href'),
        url = window.location.pathname;
    if(url.includes(href)){
        $(e).addClass('active').parent().addClass('show').prev().removeClass('collapsed').attr('aria-expanded', true);
    }
});
