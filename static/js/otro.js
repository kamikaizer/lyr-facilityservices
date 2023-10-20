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
      }
    }
  });
  }
}