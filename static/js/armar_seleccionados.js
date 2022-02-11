function armar_seleccionados(multiple) {
     var inputs = document.getElementsByTagName('input');
     var seleccion = "";
     var id;
     var elemento = ((multiple == 'm') ? 'checkbox' : 'radio');
     for (var i = 0; i < inputs.length; i++) {
         if (inputs[i].type == elemento) {
             if (inputs[i].checked == true) {
                id = inputs[i].id ;
                seleccion = seleccion + ((seleccion.length == 0) ? '' : ';') + id ;
                if (multiple != 'm') {
                    break;
                }
             }
         }
     }
     if (seleccion.length > 0) {
        window.opener.setValue(seleccion);
        close();
     } else {
        alert('No se seleccionó ningún item');
     }
 }
