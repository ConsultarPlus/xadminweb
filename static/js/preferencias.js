function fijar_menu(usuario, url) {
    var fijar_menu = document.getElementById("fijar_menu");
    var fijar = fijar_menu.attributes.data.value;

    if (fijar == "true") {
        fijar = "false"
        toggle = "off"
    } else {
        fijar = "true"
        toggle = "on"
    }
    $.ajax({
          url: url,
          data: {'usuario': usuario,
                 'vista': 'menu',
                 'opcion': 'fijar',
                 'logico': fijar},
          success: function (data) {
            if (data["resultado"] == true) {
                fijar_menu.attributes.data.value = fijar;
                var fijar_icono = document.getElementById("fijar_icono");
                fijar_icono.className  = "fa fa-toggle-" + toggle;

            }
          }
        });

}

function fijar_boton_menu(usuario, url, id_grupo, fijar) {
    $.ajax({
          url: url,
          data: {'usuario': usuario,
                 'vista': 'menu',
                 'opcion': id_grupo,
                 'logico': fijar},
          success: function (data) {
            if (data["resultado"] == true) {
                //nada
            }
          }
        });

}


function estilo_menu(usuario, url) {
    var obj = document.getElementById("modo_obscuro");
    var icono = document.getElementById("icono_modo_obscuro");
    var modo_obscuro = obj.attributes.data.value;
    if (modo_obscuro == 'false') {
        modo_obscuro = true;
        toggle = "on"
        obj.attributes.data.value = 'true';
        obj.attributes.title.value = 'Estilo claro';
    } else {
        modo_obscuro = false;
        toggle = "off"
        obj.attributes.data.value = 'false';
        obj.attributes.title.value = 'Estilo obscuro';
    }
    $.ajax({
          url: url,
          data: {'usuario': usuario,
                 'vista': 'menu',
                 'opcion': 'modo_obscuro',
                 'logico': modo_obscuro},
          success: function (data) {
            if (data["resultado"] == true) {
                icono.className  = "fa fa-toggle-" + toggle;
                refreshCSS();
            }
          }
        });
}

function refreshCSS() {
    let links = document.getElementsByTagName('link');
    for (let i = 0; i < links.length; i++) {
        if (links[i].getAttribute('rel') == 'stylesheet') {
            let id = links[i].getAttribute('id');
            if (id=='css_sidebar' || id=='css_base') {
                let href = links[i].getAttribute('href');
                if (href.search('_dark')<0) {
                    var newHref = href.replace('.css', '_dark.css');
                    document.getElementById("pop-cuerpo").style.background = "#333333";
                } else {
                    var newHref = href.replace('_dark.css', '.css');
                    document.getElementById("pop-cuerpo").style.background = "white";
                }
                links[i].setAttribute('href', newHref);
            }
        }
    }
}

function insumido_tools_agrupado(usuario, url, agrupar) {
    $.ajax({
          url: url,
          data: {'usuario': usuario,
                 'vista': 'insumidos_listar',
                 'opcion': 'agrupar_botones',
                 'logico': agrupar},
        success: function (data) {
            if (data["resultado"] == true) {
            }
        }
    });
    var div_agrupado = document.getElementById("id_agrupado");
    var div_desagrupado = document.getElementById("id_desagrupado");
    if (agrupar == true){
        div_agrupado.style.display = 'block';
        div_desagrupado.style.display = 'none';
    } else {
        div_agrupado.style.display = 'none';
        div_desagrupado.style.display = 'block';
    }
}
