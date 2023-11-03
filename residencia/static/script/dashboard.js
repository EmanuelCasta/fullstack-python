



let removeCedulaBtn = document.getElementById('removeCedula');

if (removeCedulaBtn) {  // Verifica si el elemento existe
  removeCedulaBtn.addEventListener('click', function() {
      const cedulaList = document.getElementById('cedula-list');
      if (cedulaList && cedulaList.children.length > 1) {  // Asegúrate de que cedulaList también exista
          cedulaList.removeChild(cedulaList.lastChild);
      }
  });
}




'use strict';
document.addEventListener('click', function(event) {
  let clickedFormSection = null;

  // Verifica si el clic fue dentro de alguna sección
  for (let target = event.target; target && target !== this; target = target.parentNode) {
      if (target.matches('.form-section')) {
          clickedFormSection = target;
          break;
      }
  }

  // Si se hizo clic en una form-section, oculta las demás
  if (clickedFormSection) {
      const sections = document.querySelectorAll('.form-section');
      sections.forEach(section => {
          if (section !== clickedFormSection) {
              section.classList.add('inactive');
          } else {
              section.classList.remove('inactive');
          }
      });
  }
  // Si se hizo clic fuera de cualquier form-section, muestra todas
  else {
      const sections = document.querySelectorAll('.form-section');
      sections.forEach(section => {
          section.classList.remove('inactive');
      });
  }
});

document.addEventListener('click', function(event) {
  let clickedFormSection = null;

  // Verifica si el clic fue dentro de alguna sección
  for (let target = event.target; target && target !== this; target = target.parentNode) {
      if (target.matches('.form-section')) {
          clickedFormSection = target;
          break;
      }
  }

  // Si se hizo clic en una form-section, oculta las demás y centra la clickeada
  if (clickedFormSection) {
      const sections = document.querySelectorAll('.form-section');
      sections.forEach(section => {
          if (section !== clickedFormSection) {
              section.classList.add('inactive');
              section.classList.remove('centered');
          } else {
              section.classList.remove('inactive');
              section.classList.add('centered');
          }
      });
  }
  // Si se hizo clic fuera de cualquier form-section, muestra todas y quita el centrado
  else {
      const sections = document.querySelectorAll('.form-section');
      sections.forEach(section => {
          section.classList.remove('inactive', 'centered');
      });
  }
});

document.addEventListener('click', function(event) {
  let clickedFormSection = null;

  // Verifica si el clic fue dentro de alguna sección
  for (let target = event.target; target && target !== this; target = target.parentNode) {
      if (target.matches('.form-section')) {
          clickedFormSection = target;
          break;
      }
  }

  // Si se hizo clic en una form-section, oculta las demás y centra la clickeada
  if (clickedFormSection) {
      const sections = document.querySelectorAll('.form-section');
      sections.forEach(section => {
          if (section !== clickedFormSection) {
              section.classList.add('inactive');
              section.classList.remove('centered', 'active');
          } else {
              section.classList.remove('inactive');
              section.classList.add('centered', 'active');
          }
      });
  }
  // Si se hizo clic fuera de cualquier form-section, muestra todas y quita el centrado y la opacidad alta
  else {
      const sections = document.querySelectorAll('.form-section');
      sections.forEach(section => {
          section.classList.remove('inactive', 'centered', 'active');
      });
  }
});





const header = document.querySelector("[data-header]");
const navToggleBtn = document.querySelector("[data-menu-toggle-btn]");

navToggleBtn.addEventListener("click", function () {
  header.classList.toggle("active");
});

function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}




$('#eviaButton').click(function() {
  var csrfToken = getCookie('token');
  if (!csrfToken || csrfToken.trim() === "") {
    window.location.href = '/residencia/sesion/';
  }
  
});

/**
 * toggle ctx-menu when click on card-menu-btn
 */

const menuBtn = document.querySelectorAll("[data-menu-btn]");

for (let i = 0; i < menuBtn.length; i++) {
  menuBtn[i].addEventListener("click", function () {
    this.nextElementSibling.classList.toggle("active");
  });
}



/**
 * load more btn loading spin toggle
 */

const loadMoreBtn = document.querySelector("[data-load-more]");

loadMoreBtn.addEventListener("click", function () {
  this.classList.toggle("active");
});

