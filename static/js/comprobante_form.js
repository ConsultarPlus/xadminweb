var myWindow;
var entidad_global;
window.addEventListener('unload', function(event) {
    myWindow.close();
});

function openWin(entidad) {
  if (entidad == 1) {
    var url = $("#urlsForm").attr("seleccionar_institucion-url");
  } else {
    if (entidad == 2) {
      var url = $("#urlsForm").attr("seleccionar_expedientes_padres-url");
    } else {
      var url = $("#urlsForm").attr("seleccionar_plantilla-url");
    }
  }
  entidad_global = entidad ;
  if (myWindow) {
    myWindow.close();
  }
  myWindow = window.open(url, "_blank", "height=900, width=800, status=yes, toolbar=no, " +
                         "menubar=no, location=no, addressbar=no");
}
function setValue(seleccion) {
    if (entidad_global == 1) {
      var url = $("#urlsForm").attr("institucion_nombre-url");
    } else {
      if (entidad_global == 2) {
        var url = $("#urlsForm").attr("expediente_numero-url");
      } else {
        var url = $("#urlsForm").attr("plantilla_contenido-url");
      }
    }
    var nombre = ""
    $.ajax({
          url: url,
          data: {'id': seleccion},
          success: function (data) {
            if (entidad_global == 1) {
              nombre = data["nombre"];
              var select = $('#id_institucion');
              $('option', select).remove();
              $('#id_institucion').append('<option value="' + seleccion + '" selected="selected">' + nombre + '</option>');
            } else {
                if (entidad_global == 2) {
                  var select = $('#id_expedientes');
                  const object = data
                  for (const [key, value] of Object.entries(object)) {
                    console.log(key, value);
                    var agregar = 'S';
                    var selectobject=document.getElementById("id_expedientes")
                    for (var i=0; i<selectobject.length; i++){
                      valor = selectobject.options[i].value;
                      console.log("valor: " + valor);
                      if (valor == key) {
                        agregar = 'N';
                        break;
                      }
                    }
                    if (agregar == 'S') {
                      $('#id_expedientes').append('<option value="' + key + '" selected="selected">' + value + '</option>');
                    }
                  }
                } else {
                  contenido = data["contenido"];
                  tinymce.activeEditor.setContent(contenido);
                }
            }
          }
    });
    if (entidad_global == 1) {
      var url = $("#urlsForm").attr("cargar_responsables_de_institucion-url");
      $.ajax({
            url: url,
            data: {'id': seleccion},
            success: function (data) {
            $("#id_persona").html(data);
          }
      });
    }
}

function closeWin() {
  myWindow.close();
}