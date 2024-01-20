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

  $('#agrega_clientes').on("submit", function (event) {
    
    event.preventDefault();
    $.ajax({
      url: "/agrega_clientes",
      method: "POST",
      data: $('#agrega_clientes').serialize(),
      beforeSend: function () {
        $('#agrega_clientes').val("Inserting");
      },
      success: function (data) {
        if (data == 'success') {
          $("#div_cliente").load(window.location.href + " #div_cliente");

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

  // $('#insert_oc').on("submit", function (event) {
    
  //   event.preventDefault();
  //   $.ajax({
  //     url: "/insert_oc",
  //     method: "POST",
  //     data: $('#insert_oc').serialize(),
  //     beforeSend: function () {
  //       $('#insert_oc').val("Inserting");
  //     },
  //     success: function (data) {
  //       if (data == 'success') {
  //         alert("Orden de compra agregada");
  //         window.location.href = 'aprobar'
  //       }
  //     }
  //   });

  // });

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

  $('#update_cliente').on("submit", function (event) {
    
    event.preventDefault();
    $.ajax({
      url: "/update_cliente",
      method: "POST",
      data: $('#update_cliente').serialize(),
      beforeSend: function () {
        $('#update_cliente').val("Inserting");
      },
      success: function (data) {
        if (data == 'success') {
          alert("Cliente actualizado");
          window.close()
          $("#div_cliente").load(window.location.href + " #div_cliente");
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

  function rechazo_cotizacion(id){
    if(confirm('¿Seguro que desea eliminar la cotización N°'+id+'?')){
      event.preventDefault();
    $.ajax({
      url: "/delete_cotizacion?id="+id,
      method: "POST",
      success: function (data) {
        if (data == 'success') {
          alert("Cotización Rechazada");
          $("#aprobar_cot").load(window.location.href + " #aprobar_cot");
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


function delete_cliente(id){
  if(confirm('¿Seguro que desea eliminar el cliente N° '+id+'?')){
    event.preventDefault();
  $.ajax({
    url: "/delete_cliente?id="+id,
    method: "POST",
    success: function (data) {
      if (data == 'success') {
        alert("Cliente eliminado");
        $("#div_cliente").load(window.location.href + " #div_cliente");

      }
    }
  });
  }
}

function delete_rendicion(id){
  if(confirm('¿Seguro que desea eliminar la rendicion de gastos N° '+id+'?')){
    event.preventDefault();
  $.ajax({
    url: "/delete_rendicion?id="+id,
    method: "POST",
    success: function (data) {
      if (data == 'success') {
        alert("Rendicion eliminada");
        $("#rendicion").load(window.location.href + " #rendicion");

      }
    }
  });
  }
}

function delete_inventario(id){
  if(confirm('¿Seguro que desea eliminar el elemento N° '+id+'?')){
    event.preventDefault();
  $.ajax({
    url: "/delete_inventario?id="+id,
    method: "POST",
    success: function (data) {
      if (data == 'success') {
        alert("Elemento eliminado");
        $("#inventario").load(window.location.href + " #inventario");

      }
    }
  });
  }
}



// $('#agrega_gastos').on("submit", function (event) {
//   event.preventDefault();
//   $.ajax({
//     url: "/agrega_gastos",
//     method: "POST",
//     data: $('#agrega_gastos').serialize(),
//     beforeSend: function () {
//       $('#agrega_gastos').val("Inserting");
//     },
//     success: function (data) {
//       if (data == 'success') {
//         alert("Gasto agregado");
//         window.location.href = 'gastos'
//       }
//     }
//   });

// });

$('#agrega_gastos').on("submit", function(event) {
  event.preventDefault();

  var formData = new FormData(this); // Usa FormData para manejar los datos del formulario y el archivo

  $.ajax({
      url: "/agrega_gastos",
      method: "POST",
      data: formData,
      processData: false,  // Indica a jQuery que no procese los datos
      contentType: false,  // Indica a jQuery que no establezca el tipo de contenido
      beforeSend: function() {
          $('#agrega_gastos').val("Inserting");
      },
      success: function(data) {
          if (data == 'success') {
            alert("Gasto agregado");
            window.location.href = 'gastos'
          }
          else{
            alert("Fail");
          }
      }
  });
});

$('#agrega_inventario').on("submit", function (event) {
  event.preventDefault();
  $.ajax({
    url: "/agrega_inventario",
    method: "POST",
    data: $('#agrega_inventario').serialize(),
    beforeSend: function () {
      $('#agrega_inventario').val("Inserting");
    },
    success: function (data) {
      if (data == 'success') {
        alert("Item agregado");
        window.location.href = 'inventario'
      }
    }
  });

});

$('#datos_servicios').on("submit", function (event) {
  event.preventDefault();
  $.ajax({
    url: "/datos_servicios",
    method: "POST",
    data: $('#datos_servicios').serialize(),
    beforeSend: function () {
      $('#datos_servicios').val("Inserting");
    },
    success: function (data) {
      if (data == 'success') {
        alert("Servicio agregado");
        window.location.href = 'gastos_clientes'
      }
    }
  });

});