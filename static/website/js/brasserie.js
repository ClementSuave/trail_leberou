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
/*
window.sr = ScrollReveal({reset:true});

  sr.reveal('.row.section', {
    distance: '20px',
    duration: 500,
    easing: 'ease',
    mobile: false,
    reset: false,
    viewFactor: 0.4,
  });
*/
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


//animation bouteilles footer on scroll

const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    const bouteille = entry.target.querySelector('#bouteilles_footer');

    if (entry.isIntersecting) {
      bouteille.classList.add('bouteille_animation');
    return; // if we added the class, exit the function
    }

    // We're not intersecting, so remove the class!
    bouteille.classList.remove('bouteille_animation');
  });
});

observer.observe(document.querySelector('footer'));

//animation Eglises on scroll

const eglises_obs = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    const eglises = entry.target.querySelector('#eglises_carte');

    if (entry.isIntersecting) {
      eglises.classList.add('eglises_animation');
    return; // if we added the class, exit the function
    }

    // We're not intersecting, so remove the class!
    eglises.classList.remove('eglises_animation');
  });
});

eglises_obs.observe(document.querySelector('#eglises_carte_container'));

//animation loup on scroll

const loup_obs = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    const loup = entry.target.querySelector('#leberou_transf');

    if (entry.isIntersecting) {
      loup.classList.add('leberou_transf_animation');
    return; // if we added the class, exit the function
    }

    // We're not intersecting, so remove the class!
    loup.classList.remove('leberou_transf_animation');
  });
});

loup_obs.observe(document.querySelector('#leberou_transf_container'));


//------------------------------- IV Elements --------------------------------------------
(function () {
  // Add event listener
  document.addEventListener("mousemove", parallax2);
  const elem = $("#iv-elements_logo");
  // Magic happens here
  function parallax2(e) {
    let _w = window.innerWidth / 2;
    let _h = window.innerHeight / 2;
    
    let _mouseX = e.clientX;
    let _mouseY = e.clientY;

    let _depth2 = "50% 40%"; //eau
    let _depth3 = "40% 50%"; //blé
    let _depth4 = "60% 50%"; //levure
    let _depth5 = "50% 60%"; //houblon
    
    let x = `${_depth2}, ${_depth3}, ${_depth4}, ${_depth5}`;

    if ($('#iv-elements:hover').length != 0) {
    	$("#iv-elements_logo").css({backgroundPosition: x});
	}
	else {
		$("#iv-elements_logo").css({backgroundPosition: "50% 50%, 50% 50%, 50% 50%"});
	}
  }
})();

//------------------------------- Equilibrium - brasserie --------------------------------------------
(function () {
  // Add event listener
  document.addEventListener("mousemove", parallax3);
  const elem = $("#equilibrium_logo");
  // Magic happens here
  function parallax3(e) {
    let _w = window.innerWidth / 2;
    let _h = window.innerHeight / 2;
    
    let _mouseX = e.clientX;
    let _mouseY = e.clientY;

    let _depth1 = `${50 - (_mouseX - _w) * 0.1}% ${50 - (_mouseY - _h) * 0.15}%`; 
    let _depth2 = `${50 + (_mouseX - _w) * 0.05}% ${50 + (_mouseY - _h) * 0.15}%`; 
    
    let x = `${_depth1}, ${_depth2}`;

    if ($('#equilibrium:hover').length != 0) {
    	$("#equilibrium_logo").css({backgroundPosition: x});
	}
	else {
		$("#equilibrium_logo").css({backgroundPosition: "50% 50%, 50% 50%"});
	}
  }
})();




});
