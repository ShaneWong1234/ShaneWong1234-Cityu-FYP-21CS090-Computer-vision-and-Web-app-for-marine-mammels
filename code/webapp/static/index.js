window.addEventListener('load', uploadPreview, false);

function uploadPreview(){
   const upload_files = document.getElementById("uploader");
   upload_files.addEventListener("change", image_previewing, false);
}



function image_previewing(){
    var amount_of_files = this.files.length;
    document.getElementById("indicator").innerHTML = "";
    document.getElementById("inner").innerHTML = "";

    for(var i=0; i < amount_of_files; i++){
        $('.carousel-inner').append("<div class='carousel-item'> <img class='d-block w-100' src='"+URL.createObjectURL(this.files[i])+"'></div>");
    }
    for(var i=0; i < amount_of_files; i++){
        $('.carousel-indicators').append("<button type='button' data-bs-target='#preview' data-bs-slide-to='"+String(i)+"' class='indicators-item' aria-label='Slide "+String(i)+"'></button>");
    }
    $(".carousel-item:first").addClass("active");
    $(".indicators-item:first").addClass("active");
    $(".indicators-item:first").attr("aria-current","true");
};

var myCarousel = document.querySelector('#preview')
var carousel = new bootstrap.Carousel(myCarousel, {
    interval:false
});

