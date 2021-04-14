function mostrarMapa(localidad, calle, altura) {
    var mapa = document.getElementById("gmap_canvas");
    mapa.src="https://maps.google.com/maps?q=" + calle + "%20" + altura + "%20" + localidad + "&t=&z=13&ie=UTF8&iwloc=&output=embed";
    document.getElementById('mapa_pop').style.display='block';
}