$("#id_grupo").change(function () {
    vaciar_lista('id_usuario');
    cargar_usuarios()
});

$("#id_tipo_insumido").change(function () {
    vaciar_lista('id_usuario');
    cargar_usuarios()
});

function cargar_usuarios(){
  var url = $("#urlsForm").attr("cargar_usuarios_de_grupo-url");  // obtiene la url de la vista `cargar_usuarios_de_grupo`
  var id = $("#id_grupo").val();  // obtiene el código del input de HTML
  var tipo = $("#id_tipo_insumido").val();  // obtiene el código del input de HTML
    $.ajax({                 // Inicializa el request de AJAX
          url: url,          // setea la url del request (= localhost:8000/tabla/cargar_usuarios_de_grupo/)
          data: {'id': id, 'tipo_insumido' : tipo},  // agrega el codigo en los parámetros del GET
          success: function (data) {    // `data` es lo que devuelve la función `cargar_usuarios_de_grupo`
          $("#id_usuario").html(data);  // recargar la lista de usuarios
          $("#id_usuario").selectpicker('refresh');
        }
    });
}

function vaciar_lista(nombre_lista) {
    var select = document.getElementById(nombre_lista);
    var length = select.options.length;
    for (i = length-1; i >= 0; i--) {
      select.options[i] = null;
      //select.options[i].remove();
    }
}
