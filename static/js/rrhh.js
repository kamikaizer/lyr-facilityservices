$(document).ready(function () {
  $('#creacion_usuario').on("submit", function (event) {
    event.preventDefault();
    $.ajax({
      url: "/register",
      method: "POST",
      data: $('#creacion_usuario').serialize(),
      beforeSend: function () {
        $('#creacion_usuario').val("Inserting");
      },
      success: function (data) {
        if (data == 'success') {
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
  

})