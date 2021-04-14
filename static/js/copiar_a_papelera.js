function copiar_a_papelera(elemento_id) {
    var str = document.getElementById(elemento_id).value;
    const el = document.createElement('textarea');
    el.value = str;
    el.setAttribute('readonly', '');
    el.style.position = 'absolute';
    el.style.left = '-9999px';
    document.body.appendChild(el);
    el.select();
    document.execCommand('copy');
    document.body.removeChild(el);
}


function copiar_etiqueta() {
    copiar_a_papelera('id_etiqueta');
}