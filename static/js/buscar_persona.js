var id_nro_doc_aux; //define variable global para usar como bandera
var id_tipo_doc_aux; //define variable global para usar como bandera
$("#id_nro_doc").focusout(function () {
    var isDisabled = $('id_nro_doc').prop('disabled');
    if (!isDisabled) {
        var url = $("#urlsForm").attr("existe_persona-url");  // obtiene la url de la vista `existe_persona`
        var url_editar = $("#urlsForm").attr("persona_editar-url");  // obtiene la url de la vista `persona_editar`
        var agregando_expediente = $("#urlsForm").attr("agregando_expediente");  // ver si es alta de expediente o solo de persona
        var modo = $("#urlsForm").attr("modo");  // ver si es alta de expediente o solo de persona
        var id_nro_doc = $(this).val();  // obtiene el número del input de HTML
        var id_tipo_doc = document.getElementById("id_tipo_doc").value; // obtiene el tipo de documento del input de HTML

        if (id_nro_doc_aux != id_nro_doc || id_tipo_doc_aux != id_tipo_doc) {
            id_nro_doc_aux = id_nro_doc;
            id_tipo_doc_aux = id_tipo_doc;
             $.ajax({
                type: 'GET' ,
                url: url,
                data: {"nro_doc": id_nro_doc, "tipo_doc":id_tipo_doc},
                success: function (response) {
                    if(response["existe"]){
                        //alert("Ya existe una persona con el mismo documento");
                        if (confirm("Ya existe una persona con el mismo documento ¿Editar?") == true){
                            var id = response["id"];
                            var queryString = window.location.search;
                            var urlParams = new URLSearchParams(queryString);
                            var origen = urlParams.get('origen');

                            url_editar += "?id=" +id + '&agregando_expediente='
                                       + agregando_expediente + '&modo=' + modo;
                            if (origen != '') {
                                url_editar += '&origen=' + origen;
                            }
                            window.location.replace(url_editar);
                        } else {
                            document.getElementById("id_nro_doc").value = response["numero"];
                            document.getElementById("id_nro_doc").focus();
                            id_nro_doc_aux = response["numero"];
                        }
                    } else {
                        //document.getElementById("id_apellido").value = response["apellido"];
                        //document.getElementById("id_nombre").value = response["nombre"];
                        //document.getElementById("id_nro_doc").value = response["numero"];
                        //document.getElementById("id_fecha_nacimiento").value = response["fecha_nacimiento"];
                        id_nro_doc_aux = response["numero"];
                    }
                },
                error: function (response) {
                    console.log(response)
                }
            });
        }
    }
});

$("#id_qr").focusout(function () {
    var id_qr = $(this).val();  // obtiene el número del input de HTML
    if (id_qr != ""){
        var id_tipo_doc = document.getElementById("id_tipo_doc").value; // obtiene el tipo de documento del input de HTML
        var url = $("#urlsForm").attr("existe_persona-url");  // obtiene la url de la vista `existe_persona`
        var url_editar = $("#urlsForm").attr("persona_editar-url");  // obtiene la url de la vista `persona_editar`
        var agregando_expediente = $("#urlsForm").attr("agregando_expediente");  // ver si es alta de expediente o solo de persona
        $.ajax({
            type: 'GET' ,
            url: url,
            data: {"nro_doc": id_qr, "tipo_doc":id_tipo_doc},
            success: function (response) {
                document.getElementById("id_qr").value = "";
                if(response["existe"]){
                    alert("Ya existe una persona con el mismo documento");
                    var id = response["id"]
                    url_editar += "?id=" +id + '&agregando_expediente=' + agregando_expediente
                    window.location.replace(url_editar)
                } else {
                    document.getElementById("id_apellido").value = response["apellido"];
                    document.getElementById("id_nombre").value = response["nombre"];
                    document.getElementById("id_nro_doc").value = response["numero"];
                    document.getElementById("id_fecha_nacimiento").value = response["fecha_nacimiento"];
                    id_nro_doc_aux = response["numero"];

                    id_nro_doc_aux = id_nro_doc;
                    id_tipo_doc_aux = id_tipo_doc;
                }
            },
            error: function (response) {
                console.log(response)
            }
        })
    };
});

function tempAlert(msg,duration)
{
 var popup = document.createElement("div");
 popup.setAttribute("style","position:absolute;top:10%;left:20%;");
 popup.setAttribute("class","alert alert-info");
 popup.innerHTML = msg;
 setTimeout(function(){
  popup.parentNode.removeChild(popup);
 },duration);
 document.body.appendChild(popup);
}

