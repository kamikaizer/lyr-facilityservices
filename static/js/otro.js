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
          $("#c1").load(window.location.href + " #c1");
          $("#c1_bruto").load(window.location.href + " #c1_bruto");
        }
      }
    });

  });



    $('#datos_cotizacion').on("submit", function (event) {
      event.preventDefault();
      $.ajax({
        url: "/datos_cotizacion",
        method: "POST",
        data: $('#datos_cotizacion').serialize(),
        beforeSend: function () {
          $('#datos_cotizacion').val("Inserting");
        },
        success: function (data) {
          if (data == 'success') {
            alert("Cotización agregada al panel de edición");
            window.location.href = 'crud'
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
          $("#totales_mano_obra").load(window.location.href + " #totales_mano_obra");
          $("#c1").load(window.location.href + " #c1");
          $("#c1_bruto").load(window.location.href + " #c1_bruto");
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

  $('#update_materiales').on("submit", function (event) {
    
    event.preventDefault();
    $.ajax({
      url: "/update_materiales",
      method: "POST",
      data: $('#update_materiales').serialize(),
      beforeSend: function () {
        $('#update_materiales').val("Inserting");
      },
      success: function (data) {
        if (data == 'success') {
          alert("Material actualizado");
          window.close()
          $("#materiales").load(window.location.href + " #materiales");
          $("#div_totales").load(window.location.href + " #div_totales");
          $("#c1").load(window.location.href + " #c1");
          $("#c1_bruto").load(window.location.href + " #c1_bruto");
          
        }
      }
    });

  });

  $('#update_mano_obra').on("submit", function (event) {
    
    event.preventDefault();
    $.ajax({
      url: "/update_mano_obra",
      method: "POST",
      data: $('#update_mano_obra').serialize(),
      beforeSend: function () {
        $('#update_mano_obra').val("Inserting");
      },
      success: function (data) {
        if (data == 'success') {
          alert("Mano de Obra actualizada");
          window.close()
          $("#div_mano_obra").load(window.location.href + " #div_mano_obra");
          $("#totales_mano_obra").load(window.location.href + " #totales_mano_obra");
          $("#c1").load(window.location.href + " #c1");
          $("#c1_bruto").load(window.location.href + " #c1_bruto");
          
        }
      }
    });

  });


})

function delete_cotizacion(id){
    if(confirm('¿Seguro que desea eliminar la cotización N°'+id+'?')){
      event.preventDefault();
    $.ajax({
      url: "/delete_cotizacion?id="+id,
      method: "POST",
      success: function (data) {
        if (data == 'success') {
          alert("Cotización Eliminada");
          $("#cotizaciones").load(window.location.href + " #cotizaciones");
        }
      }
    });
    }
  }
  
function delete_material(id){
  if(confirm('¿Seguro que desea eliminar el Material N°'+id+'?')){
    event.preventDefault();
  $.ajax({
    url: "/delete_material?id="+id,
    method: "POST",
    success: function (data) {
      if (data == 'success') {
        alert("Material Eliminado");
        $("#materiales").load(window.location.href + " #materiales");
        $("#div_totales").load(window.location.href + " #div_totales");
        $("#c1").load(window.location.href + " #c1");
        $("#c1_bruto").load(window.location.href + " #c1_bruto");
      }
    }
  });
  }
}

function delete_mano_obra(id){
  if(confirm('¿Seguro que desea eliminar la Mano de Obra N°'+id+'?')){
    event.preventDefault();
  $.ajax({
    url: "/delete_mano_obra?id="+id,
    method: "POST",
    success: function (data) {
      if (data == 'success') {
        alert("Mano de Obra Eliminada");
        $("#div_mano_obra").load(window.location.href + " #div_mano_obra");
        $("#totales_mano_obra").load(window.location.href + " #totales_mano_obra");
        $("#c1").load(window.location.href + " #c1");
        $("#c1_bruto").load(window.location.href + " #c1_bruto");
      }
    }
  });
  }
}