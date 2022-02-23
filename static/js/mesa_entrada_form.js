var myWindow;
var entidad_global;
window.addEventListener('unload', function(event) {
    myWindow.close();
});

function openWin(entidad) {
  if (entidad == 1) {
    var url = $("#urlsForm").attr("seleccionar_expediente-url");
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
        var url = $("#urlsForm").attr("expediente_numero-url");
    }
    var nombre = ""
    $.ajax({
          url: url,
          data: {'id': seleccion},
          success: function (data) {
            if (entidad_global == 1) {
              var select = $('#id_expediente');
              const object = data
              var agregar = 'S';
              if (agregar == 'S') {
//                alert("key: " + Object.keys(object));
//                alert("value: " + Object.values(object));
                $('#id_expediente').append('<option value="' + Object.keys(object) + '" selected>' + Object.values(object) + '</option>');
                $("#id_expediente").selectpicker('refresh');
              }
            }
          }
    });
}

function closeWin() {
  myWindow.close();
}