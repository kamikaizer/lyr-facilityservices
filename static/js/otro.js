$(document).ready(function () {
  $('#material').on("submit", function (event) {
    event.preventDefault();
    $.ajax({
      url: "/material",
      method: "POST",
      data: $('#material').serialize(),
      beforeSend: function () {
        $('#material').val("Inserting");
      },
      success: function (data) {
        if (data == 'success') {
          $("#div_materiales").load(window.location.href + " #div_materiales");
        }
      }
    });

  });

  $('#mano_obra').on("submit", function (event) {
    
    event.preventDefault();
    $.ajax({
      url: "/mano_obra",
      method: "POST",
      data: $('#mano_obra').serialize(),
      beforeSend: function () {
        $('#mano_obra').val("Inserting");
      },
      success: function (data) {
        if (data == 'success') {
          $("#div_mano_obra").load(window.location.href + " #div_mano_obra");
        }
      }
    });

  });

  $('#aprobar').on("submit", function (event) {
    
    event.preventDefault();
    $.ajax({
      url: "/aprobar_cotizacion",
      method: "POST",
      data: $('#aprobar').serialize(),
      beforeSend: function () {
        $('#aprobar').val("Inserting");
      },
      success: function (data) {
        if (data == 'success') {
          alert("Cotización Terminada, pasa a Etapa de Aprobación");
          window.location.href = 'crud'
        }
      }
    });

  });

})