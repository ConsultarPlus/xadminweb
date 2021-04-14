function abrir_url(url, atributo_id, target) {
     atributo_id = atributo_id || "id";

     var inputs = document.getElementsByTagName('input');
     var parametro = "";
     var id;
     for (var i = 0; i < inputs.length; i++) {
         if (inputs[i].type == 'radio') {
             if (inputs[i].checked == true) {
                if (atributo_id == "id") {
                    id = inputs[i].id ;
                } else {
                    id = inputs[i].attributes[atributo_id].value;
                }
                parametro = id ;
                break;
             }
         }
     }
     if (parametro.length > 0) {
        url += parametro
        if (target == '_blank'){
            window.open(url) ;
        } else {
            window.location.href = url ;
        }
     } else {
        alert('No se seleccionó ningún item');
     }
 }


function url_con_parametro_seleccionado(url, atributo_id) {
    abrir_url(url, atributo_id, '');
 }

function url_con_parametro_seleccionado_en_nueva_tab(url, atributo_id) {
    abrir_url(url, atributo_id, '_blank');
}