$(document).ready(function () {
  $('#creacion_usuario').on("submit", function (event) {
    event.preventDefault();
    $.ajax({
      url: "/insert_register",
      method: "POST",
      data: $('#creacion_usuario').serialize(),
      beforeSend: function () {
        $('#creacion_usuario').val("Inserting");
      },
      success: function (data) {
        if (data == 'success') {
          alert("Usuario Creado");
          $("#div_creacion_usuario").load(window.location.href + " #div_creacion_usuario");
        }
      }
    });

  });

  // $('#sol_vacaciones').on("submit", function (event) {
  //   alert("ingreso");
  //   event.preventDefault();
  //   $.ajax({
  //     url: "/sol_vacaciones",
  //     method: "POST",
  //     data: $('#sol_vacaciones').serialize(),
  //     beforeSend: function () {
  //       $('#sol_vacaciones').val("Inserting");
  //     },
  //     success: function (data) {
  //       if (data == 'success') {
  //         alert("Solicitud de vacaciones ingresada");
  //         $("#vacaciones").load(window.location.href + " #vacaciones");
  //       }
  //     }
  //   });

  // });
  
  $('#update_users').on("submit", function (event) {
    
    event.preventDefault();
    $.ajax({
      url: "/update_users",
      method: "POST",
      data: $('#update_users').serialize(),
      beforeSend: function () {
        $('#update_users').val("Inserting");
      },
      success: function (data) {
        if (data == 'success') {
          alert("Usuario actualizado");
          window.close()
          $("#div_creacion_usuario").load(window.location.href + " #div_creacion_usuario");
          
        }
      }
    });

  });

})
function delete_user(id){
  if(confirm('¿Seguro que desea eliminar al usuario N°'+id+'?')){
    event.preventDefault();
  $.ajax({
    url: "/delete_user?id="+id,
    method: "POST",
    success: function (data) {
      if (data == 'success') {
        alert("Usuario eliminado");
        $("#div_creacion_usuario").load(window.location.href + " #div_creacion_usuario");
      }
    }
  });
  }
}