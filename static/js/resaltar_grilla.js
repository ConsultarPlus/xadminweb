$('#tab').on('click','.row1', function() {
    var id = jQuery(this).closest('tr').attr('id');
    var row = jQuery(this).closest('td').parent('table').index();
    if (row != 0 && typeof(id) != 'undefined'){
        resaltar_fila('tab', id);
    }

});

$('#tab').on('click','.row2', function() {
    var id = jQuery(this).closest('tr').attr('id');
    var row = jQuery(this).closest('td').parent('table').index();
    if (row != 0 && typeof(id) != 'undefined'){
        resaltar_fila('tab', id);
    }
});

function resaltar_fila(tab, id) {
    var srow = '';
    var table = document.getElementById(tab);
    var sel = false;
    var id_radio = '';
    for (var i = 0, row; row = table.rows[i]; i++) {
        if (srow =='row1'){
            srow='row2';
        } else {
            srow='row1';
        }
        if (row.id == id) {
            row.className='row3';
            sel = true;
        } else {
            sel = false;
            row.className=srow;
        }
    }

    var id_radio = id.replace("fila_", "");
    var inputs = document.getElementsByTagName('input');
    for (var i = 0; i < inputs.length; i++) {
        var radio_obj = inputs[i]
        if (radio_obj.type == 'radio' && radio_obj.name == 'table_radio') {
            if (inputs[i].id == id_radio) {

                inputs[i].checked = true;
            } else {
                inputs[i].checked = false;
            }
        }
    }
}