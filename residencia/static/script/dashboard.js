



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
let currentSlide = 0;
    const slides = document.querySelectorAll('.pqrs-content');
    const prevButton = document.getElementById('prev');
    const nextButton = document.getElementById('next');
  
    // Muestra el primer elemento
    if (slides.length > 0) {
      slides[0].classList.add('active');
    }
  
    function changeSlide(direction) {
      slides[currentSlide].classList.remove('active');
      currentSlide += direction;
      slides[currentSlide].classList.add('active');
    }
  
    if (prevButton) {
      prevButton.addEventListener('click', function() {
        if (currentSlide > 0) {
          changeSlide(-1);
        }
      });
    }
  
    if (nextButton) {
      nextButton.addEventListener('click', function() {
        if (currentSlide < slides.length - 1) {
          changeSlide(1);
        }
      });
    }
  
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // ¿Esta cookie comienza con el nombre que queremos?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    const token = getCookie('token');
    
$("#GenerarReporte").click(function() {


        
        const token = getCookie('token')

            $.ajax({
                type: "GET",
                url: "http://localhost:8000/residencia/reservas/listado-para-porteria/",
                headers: {'Authorization': 'Bearer ' + token},
                dataType: 'json',
                success: function(data) {
                    // Convierte el JSON a formato de hoja de cálculo
                    var ws = XLSX.utils.json_to_sheet(data);
                    var wb = XLSX.utils.book_new();
                    XLSX.utils.book_append_sheet(wb, ws, "Datos");
    
                    // Genera el archivo Excel
                    var wbout = XLSX.write(wb, {bookType:'xlsx', type:'binary'});
    
                    function s2ab(s) {
                        var buf = new ArrayBuffer(s.length);
                        var view = new Uint8Array(buf);
                        for (var i=0; i<s.length; i++) view[i] = s.charCodeAt(i) & 0xFF;
                        return buf;
                    }
    
                    // Guarda el archivo
                    saveAs(new Blob([s2ab(wbout)],{type:"application/octet-stream"}), 'datos.xlsx');
                },
                error: function() {

                    $("#responseMessage").text("Error al enviar la solicitud.");
                }
            });
        });
  

$(".add-zone-button").click(function() {
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

