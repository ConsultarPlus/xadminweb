function confirmarAccion(url, mensaje) {
    var r = confirm(mensaje);
    if (r == true) {
      window.location.replace(url);
    }
}