function colocar_foco(objeto) {
    if (typeof(objeto) != 'undefined') {
        document.getElementById(objeto).focus();
    } else {
        var tipos = ["text", "number", "radio", "select-one"];
        var inputs = document.getElementsByClassName('form-control');
        for (var i = 0; i < inputs.length; i++) {
            var input_obj = inputs[i];
            var tipo = input_obj.type;
            if (tipos.includes(tipo))  {
                if (input_obj.style.display != 'none' && input_obj.disabled != true){
                    input_obj.focus();
                    break;
                }
            }
        }
    }
}