$(function () {
  $(document).scroll(function () {
    $(".navbar-fixed-top").toggleClass('scrolled', $(this).scrollTop() > $(".jumbotron").height());
    $(".navbar-brand").toggleClass('scrolled', $(this).scrollTop() > $(".jumbotron").height());
  });

});

$(document).ready(function() {

  $('[data-toggle="tooltip"]').tooltip();

  //when small screen:

  if (window.matchMedia("(max-width: 991px)").matches) {
    //autoclose navbar 
    $(".nav-item-main-navbar").attr("data-toggle", "collapse");
    $(".nav-item-main-navbar").attr("data-target", "#navbarSupportedContent");
    //remove underline 
    $(".nav-link").removeClass("hover-underline");
  } else {
    $(".nav-item-main-navbar").removeAttr("data-toggle");
    $(".nav-item-main-navbar").removeAttr("data-target");
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
