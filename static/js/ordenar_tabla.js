var orden = "AZ";

var tabla = document.getElementById('tab');
if (tabla != null) {
    document.getElementById('tab').addEventListener('click', function(){ordenar_tabla(event)}, false);
}

function ordenar_tabla()
{
  var col = window.event.target.cellIndex;
  var row = window.event.target.parentNode.rowIndex;

  if (row == 0){
    sortTable(col);
  }
}


function sortTable(nCol) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("tab");
    switching = true;
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
        //start by saying: no switching is done:
        switching = false;
        rows = table.rows;
        /*Loop through all table rows (except the
        first, which contains table headers):*/
        for (i = 1; i < (rows.length - 1); i++) {
            //start by saying there should be no switching:
            shouldSwitch = false;
            /*Get the two elements you want to compare,
            one from current row and one from the next:*/
            x = rows[i].getElementsByTagName("TD")[nCol];
            y = rows[i + 1].getElementsByTagName("TD")[nCol];
            //check if the two rows should switch place:
            var x_val = x.innerText.toLocaleLowerCase();
            var y_val = y.innerText.toLocaleLowerCase();

            //Verificar si el tipo de dato es fecha
            var ocurrencias = x_val.match(/[/]/g);
            if (ocurrencias != null) {
                if (ocurrencias.length == 2){
                    var partes = x_val.split("/");
                    var fecha = partes[1] + "/" + partes[0] + "/" + partes[2];
                    if (isNaN(Date.parse(fecha)) == false ) {
                        x_val = Date.parse(fecha);
                        var partes = y_val.split("/");
                        var fecha = partes[1] + "/" + partes[0] + "/" + partes[2];
                        y_val = Date.parse(fecha);
                    }
                }
            } else {
                //Verificar si es numéricio
                if (isNaN(parseFloat(x_val)) == false) {
                    x_val = parseFloat(x_val);
                    y_val = parseFloat(y_val);
                }
            }

            if (orden == "AZ"){
                if (x_val > y_val) {
                    //if so, mark as a switch and break the loop:
                    shouldSwitch = true;
                    break;
                }
            } else {
                if (x_val < y_val) {
                //if so, mark as a switch and break the loop:
                shouldSwitch = true;
                break;
                }
            }
        }
        if (shouldSwitch) {
            /*If a switch has been marked, make the switch
            and mark that a switch has been done:*/
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }

    if (orden == "AZ"){
        orden = "ZA"
    } else {
        orden = "AZ"
    }

    var row_class = '';
    for (var i = 0, row; row = table.rows[i]; i++) {
        if (row_class =='row1'){
            row_class='row2';
        } else {
            row_class='row1';
        }
        if (typeof id === 'undefined') {
            if (row.className == 'row3') {
                row.className='row3';
            } else {
                row.className=row_class;
            }
        } else {
            if (row.id == id) {
                row.className='row3';
            } else {
                row.className=row_class;
            }
        }
    }

}
