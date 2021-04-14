function contar_mensajes_pendientes(usuario, url) {
    $.ajax({
          url: url,
          data: {'usuario': usuario,},
        success: function (data) {
            var pendientes = data["pendientes"]
            var mensajillo = document.getElementById("id_mensaje");
            if (pendientes == 0 ) {
                document.getElementById("id_mensaje").className = "envelope-normal";
                document.getElementById("id_mensaje_cantidad").innerHTML = "";
                document.getElementById("id_mensaje_cantidad").className = "";
            } else {
                if (pendientes > 9) {
                    pendientes = '9+';
                }
                document.getElementById("id_mensaje").className = "envelope-solid";
                document.getElementById("id_mensaje_cantidad").innerHTML = pendientes;
                document.getElementById("id_mensaje_cantidad").className = "rcorners";
            }
        }
    });
}