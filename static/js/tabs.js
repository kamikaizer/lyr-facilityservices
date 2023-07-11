// function openCity(evt, cityName) {
//   var i, tabcontent, tablinks;
//   tabcontent = document.getElementsByClassName("tabcontent");
//   for (i = 0; i < tabcontent.length; i++) {
//     tabcontent[i].style.display = "none";
//   }
//   tablinks = document.getElementsByClassName("tablinks");
//   for (i = 0; i < tablinks.length; i++) {
//     tablinks[i].className = tablinks[i].className.replace(" active", "");
//   }
//   document.getElementById(cityName).style.display = "block";
//   evt.currentTarget.firstElementChild.className += " active";
// }

// document.getElementById("defaultOpen").click();
// function investiga (URL){window.open(URL,"ventana1","width=750,height=550,scrollbars=auto")}


  // Función para cambiar el contenido según el tab seleccionado
  function showTab(tab) {
    // Obtener todos los elementos con clase "tabcontent" y ocultarlos
    var tabcontent = document.getElementsByClassName("tabcontent");
    for (var i = 0; i < tabcontent.length; i++) {
      tabcontent[i].style.display = "none";
    }
  
    // Obtener todos los elementos con clase "tablinks" y eliminar la clase "active"
    var tablinks = document.getElementsByClassName("tablinks");
    for (var i = 0; i < tablinks.length; i++) {
      tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
  
    // Mostrar el contenido del tab actual y añadir la clase "active" al botón que lo abre
    document.getElementById(tab).style.display = "block";
    event.currentTarget.className += " active";
  }
  
