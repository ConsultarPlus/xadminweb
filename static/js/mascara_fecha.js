var input = document.querySelectorAll('.js-date')[0];

var dateInputMask = function dateInputMask(elm) {
    if (elm){
        elm.addEventListener('keypress', function(e) {
            if(e.keyCode < 47 || e.keyCode > 57) {
                e.preventDefault();
            }
            var len = elm.value.length;

            // Si está en una posición particular, dejar que el usuario ponga la barra
            // ejemplo 12/12/1212
            if(len !== 1 || len !== 3) {
              if(e.keyCode == 47) {
                e.preventDefault();
              }
            }

            // Si no pone la barra, hacerlo automáticamente
            if(len === 2) {
              elm.value += '/';
            }

            // Si no pone la barra, hacerlo automáticamente
            if(len === 5) {
              elm.value += '/';
            }
        });
    };
};

dateInputMask(input);