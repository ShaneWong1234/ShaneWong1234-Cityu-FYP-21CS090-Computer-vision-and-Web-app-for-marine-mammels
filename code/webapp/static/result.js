window.addEventListener('load', resultDisplay, false);

function resultDisplay(){
    $(".carousel-item:first").addClass("active");
    $(".indicators-item:first").addClass("active");
    $(".indicators-item:first").attr("aria-current","true");

    var myCarousel = document.querySelector('#preview');
    var carousel = new bootstrap.Carousel(myCarousel, {
        interval:false
    });
}
