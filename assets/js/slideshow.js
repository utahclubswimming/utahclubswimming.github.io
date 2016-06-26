/*
Based on: http://stackoverflow.com/a/25348073
**/

var currentSlide = 0;
var slideDuration = 5000;

function slideShow() {
    setTimeout(function() {
        document.getElementById("banner-wrapper").style.backgroundImage = "url('" + imageSources[currentSlide] + "')";
    }, 0);
    currentSlide++;
    if (currentSlide == imageSources.length) { currentSlide = 0; }
    setTimeout(slideShow, slideDuration);
}

slideShow();
