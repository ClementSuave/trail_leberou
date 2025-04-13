$(function () {
  $(document).scroll(function () {
    $(".navbar-fixed-top").toggleClass('scrolled', $(this).scrollTop() > $(".jumbotron").height());
    $(".navbar-brand").toggleClass('scrolled', $(this).scrollTop() > $(".jumbotron").height());
  });

});

function deferVideo() {

  //defer html5 video loading
  $("video source").each(function() {
    var sourceFile = $(this).attr("data-src");
    $(this).attr("src", sourceFile);
    var video = this.parentElement;
    video.load();
    // uncomment if video is not autoplay
    //video.play();
  });

}
window.onload = deferVideo;

$(document).ready(function() {

  $('[data-toggle="tooltip"]').tooltip();

  //when small screen:

  if (window.matchMedia("(max-width: 991px)").matches) {
    //autoclose navbar 
    $(".nav-item").attr("data-toggle", "collapse");
    $(".nav-item").attr("data-target", "#navbarSupportedContent");
    //remove underline 
    $(".nav-link").removeClass("hover-underline");
  } else {
    $(".nav-item").removeAttr("data-toggle");
    $(".nav-item").removeAttr("data-target");
  }
  //hamburger button top
  $('.third-button').on('click', function () {
      $('.hamburger').toggleClass('open');
  });
  $('.nav-link-click').on('click', function () {
      $('.hamburger').removeClass('open');
  });

  (function () {
    // Utilisation de la directive "use strict" pour activer le mode strict en JavaScript
    // Cela implique une meilleure gestion des erreurs et une syntaxe plus stricte pour le code
    "use strict"

    // Sélectionne tous les éléments avec la classe "animate-on-scroll"
    const elements = document.querySelectorAll(".section_title,.animate-on-scroll");
    // Options pour l'observateur d'intersection
    const options = {
        threshold: 0.25
    };
    // Instanciation de l'observateur d'intersection
    const observer = new IntersectionObserver(function (entries, observer) {
        // Boucle sur chaque entrée pour traiter les intersections
        entries.forEach(entry => {
            // Si l'entrée est en train d'intersecter avec la zone visible
            if (entry.isIntersecting) {
                // Ajouter la classe "is-visible" pour déclencher l'animation
                entry.target.classList.add("is-visible");
                // Cesser d'observer cet élément
                observer.unobserve(entry.target);
            }
        });
    }, options);
    // Observer chaque élément
    elements.forEach(element => {
        observer.observe(element);
    });

  })();

});
