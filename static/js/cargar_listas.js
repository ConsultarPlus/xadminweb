///PROVINCIA///
$("#id_provincia").change(function () {
    var url = $("#urlsForm").attr("localidades-url");  // obtiene la url de la vista `cargar_localidades`
    var provincia_id = $("#id_provincia").val();  // obtiene el código de provincia del input de HTML

    $.ajax({                       // Inicializa el request de AJAX
          url: url,                    // setea la url del request (= localhost:8000/tabla/cargar_localidades/)
          data: {'id': provincia_id},  // agrega el codigo de provincia en los parámetros del GET
          success: function (data) {   // `data` es lo que devuelve la función `cargar_localidades`
            $("#id_localidad").html(data);  // recargar la lista de localidades
            $("#id_localidad").selectpicker('refresh');
          }
        });
});

///SECTORES///
$("#id_sector").change(function () {
    vaciar_lista('id_tema');
    vaciar_lista('id_subtema');
    vaciar_lista('id_subsector');
    var url = $("#urlsForm").attr("cargar_subordinados-url");  // obtiene la url de la vista `cargar_subordinados`
    var id = $("#id_sector").val();  // obtiene el código del input de HTML

    sector_id_aux = id;
    $.ajax({                 // Inicializa el request de AJAX
            url: url,          // setea la url del request (= localhost:8000/tabla/cargar_subordinados/)
            data: {'id': id},  // agrega el codigo en los parámetros del GET
            success: function (data) {    // `data` es lo que devuelve la función `cargar_subordinados`
                $("#id_subsector").html(data);  // recargar la lista de subordinados
                $('#id_subsector').selectpicker('refresh');
            }
           });

});

///SUBSECTORES///
$("#id_subsector").change(function () {
    vaciar_lista('id_tema');
    vaciar_lista('id_subtema');
    var url = $("#urlsForm").attr("cargar_subordinados-url");  // obtiene la url de la vista `cargar_subordinados`
    var id = $("#id_subsector").val();  // obtiene el código del input de HTML

    $.ajax({                 // Inicializa el request de AJAX
          url: url,          // setea la url del request (= localhost:8000/tabla/cargar_subordinados/)
          data: {'id': id},  // agrega el codigo en los parámetros del GET
          success: function (data) {    // `data` es lo que devuelve la función `cargar_subordinados`
            $("#id_tema").html(data);  // recargar la lista de subordinados
            $("#id_tema").selectpicker('refresh');
          }
        });

});

///TEMAS///
$("#id_tema").change(function () {
    var url = $("#urlsForm").attr("cargar_subordinados-url");  // obtiene la url de la vista `cargar_subordinados`
    var id = $("#id_tema").val();  // obtiene el código del input de HTML

    tema_id_aux = id;
    $.ajax({                 // Inicializa el request de AJAX
          url: url,          // setea la url del request (= localhost:8000/tabla/cargar_subordinados/)
          data: {'id': id},  // agrega el codigo en los parámetros del GET
          success: function (data) {    // `data` es lo que devuelve la función `cargar_subordinados`
            $("#id_subtema").html(data);  // recargar la lista de subordinados
            $("#id_subtema").selectpicker('refresh');
          }
    });
});

////ENTIDADES DE TABLAS///
$("#id_superior_entidad").change(function () {
    var url = $("#tablaForm").attr("cargar_registros_de_entidad-url");  // obtiene la url de la vista `cargar_registros_de_entidad`
    var entidad = $("#id_superior_entidad").val();  // obtiene el código de entidad del input de HTML

    $.ajax({                       // Inicializa el request de AJAX
      url: url,                    // setea la url del request (= localhost:8000/tabla/cargar_registros_de_entidad/)
      data: {'entidad': entidad},  // agrega el codigo de provincia en los parámetros del GET
      success: function (data) {   // `data` es lo que devuelve la función `cargar_registros_de_entidad`
        $("#id_superior_codigo").html(data);  // recargar la lista de registros de una entidad
        $("#id_superior_codigo").selectpicker('refresh');
      }
    });
});


////Etiquetas de grupo de etiquetas///
$("#id_grupo_etiquetas").change(function () {
    var url = $("#urlsForm").attr("etiquetas_de_grupo-url");  // obtiene la url de la vista `cargar_registros_de_entidad`
    var grupo = $("#id_grupo_etiquetas").val();  // obtiene el código del grupo del input de HTML

    $.ajax({                       // Inicializa el request de AJAX
      url: url,                    // setea la url del request
      data: {'grupo': grupo},  // agrega el codigo de provincia en los parámetros del GET
      success: function (data) {   // `data` es lo que devuelve la función
        $("#id_etiqueta").html(data);  // recargar la lista de registros de una entidad
        $("#id_etiqueta").selectpicker('refresh');
      }
    });
});

function vaciar_lista(nombre_lista) {
    var select = document.getElementById(nombre_lista);
    var length = select.options.length;
    for (i = length-1; i >= 0; i--) {
      select.options[i] = null;
      //select.options[i].remove();
    }
}

