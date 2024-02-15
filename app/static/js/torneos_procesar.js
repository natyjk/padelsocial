// Almacena los IDs únicos de las filas que cumplen con los filtros seleccionados
var ids_torneos = [];
// Llamada inicial para cargar el menú desplegable
document.addEventListener('DOMContentLoaded', function() {
    cargarFiltrosTorneos();
});

function cargarFiltrosTorneos() {
    // Enviar la solicitud a Flask para obtener la lista de usuarios
    fetch('/obtener_lista_torneos')
        .then(response => response.json())
        .then(data => {
            // Actualizar el menú desplegable con la lista de usuarios
            cargarOpcionesFiltro(data);
            cargarTablaTorneos(data);
        })
        .catch(error => {
            console.error('Error al obtener filtros:', error);
        });
}


// Función para cargar las opciones de los filtros desde Flask
function cargarOpcionesFiltro(data) {

    // Obtener valores únicos de la columna 'filtro1'
    var opcionesLugar = [...new Set(data.map(item => item.lugar))];

    // Obtener valores únicos de la columna 'filtro2'
    var opcionesStatus = [...new Set(data.map(item => item.status_scraping))];

    // Obtener valores únicos de la columna 'filtro3'
    var opcionesAno = [...new Set(data.map(item => item.fecha_ano))];

    // Cargar opciones en el filtro 1
    var filtroLugar = document.getElementById('filtroLugar');
    opcionesLugar.forEach(function(opcion) {
        var option = document.createElement('option');
        option.text = opcion;
        filtroLugar.add(option);
    });

    // Cargar opciones en el filtro 1
    var filtroStatus = document.getElementById('filtroStatus');
    opcionesStatus.forEach(function(opcion) {
        var option = document.createElement('option');
        option.text = opcion;
        filtroStatus.add(option);
    });

    // Cargar opciones en el filtro 1
    var filtroAno = document.getElementById('filtroAno');
    opcionesAno.forEach(function(opcion) {
        var option = document.createElement('option');
        option.text = opcion;
        filtroAno.add(option);
    });

}

// Función para ejecutar la acción al presionar el botón
function ScrapearTorneos() {
    var seleccionados = [];
    var checkboxes = document.querySelectorAll('#tabla-body input[type="checkbox"]:checked');

    checkboxes.forEach(function(checkbox) {
        var id_torneo = checkbox.dataset.idTorneo;
        seleccionados.push(id_torneo);
    });
    // Llamar a la función en Flask pasando los ids seleccionados
    console.log("Ids seleccionados:", seleccionados);
    // Aquí podrías hacer la llamada AJAX a Flask para ejecutar la función con los ids seleccionados
    // Enviar la solicitud a Flask para obtener la lista de usuarios
    fetch('/scrapear_torneos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ torneo_id: seleccionados })
    })
    .then(() => {
        // Tu código para procesar la respuesta
        console.log('Scrapeando Torneos')
    })
    .catch(error => {
        console.error('Error al obtener filtros:', error);
    });
}

// Función para cargar la tabla con los datos del DataFrame
function cargarTablaTorneos(data) {
    var tablaBody = document.getElementById('tabla-body');

    // Limpiar el cuerpo de la tabla antes de cargar nuevos datos
    tablaBody.innerHTML = '';

    // Recorrer los datos y agregar cada fila a la tabla
    data.forEach(function(fila) {
        var tr = document.createElement('tr');
        var idTorneo = fila.id_torneo;

        // Crear la celda de selección con un checkbox
        var tdSeleccion = document.createElement('td');
        var checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.setAttribute('data-id-torneo', idTorneo);
        tdSeleccion.appendChild(checkbox);
        tr.appendChild(tdSeleccion);

        // Iterar sobre las columnas y agregar celdas a la fila
        var columnas = ['fecha_ano', 'fecha_str', 'nombre_torneo', 'lugar', 'partidos', 'status_scraping']; // Agrega aquí los nombres de tus columnas
        columnas.forEach(function(columna) {
            var td = document.createElement('td');
            td.textContent = fila[columna]; // Usa el nombre de la columna correspondiente
            tr.appendChild(td);
        });
        // Agregar la fila a la tabla
        tablaBody.appendChild(tr);

        // Agregar el ID único a la lista de IDs filtrados
        ids_torneos.push(idTorneo);
    });
}

    // Llamar a la función para cargar la tabla
    // cargarTablaTorneos(data);
function filtrarTabla() {
    ids_torneos = [];
    // Obtener los valores seleccionados en los filtros
    var filtroAno = document.getElementById('filtroAno').value;
    var filtroLugar = document.getElementById('filtroLugar').value;
    var filtroStatus = document.getElementById('filtroStatus').value;

    // Obtener las filas de la tabla
    var filas = document.getElementById('tabla-body').getElementsByTagName('tr');

    // Recorrer todas las filas y mostrar u ocultar según los filtros
    for (var i = 0; i < filas.length; i++) {
        var fila = filas[i];
        var datosFila = fila.getElementsByTagName('td');

        // Obtener los valores de las columnas para esta fila
        var valorAno = datosFila[1].textContent; // Suponiendo que la columna 1 contiene el año
        var valorLugar = datosFila[4].textContent; // Suponiendo que la columna 2 contiene el lugar
        var valorStatus = datosFila[6].textContent; // Suponiendo que la columna 3 contiene el estado del torneo

        // Mostrar u ocultar la fila según los filtros seleccionados
        if ((filtroAno === '' || valorAno === filtroAno) &&
            (filtroLugar === '' || valorLugar === filtroLugar) &&
            (filtroStatus === '' || valorStatus === filtroStatus)) {
            fila.style.display = '';
        } else {
            fila.style.display = 'none';
        }
    }
}

// Función para manejar el evento de cambio del botón "Select All"
document.getElementById('select-all').addEventListener('change', function() {
    // Obtener el estado del botón "Select All"
    var isChecked = this.checked;

    // Obtener todas las filas de la tabla
    var rows = document.querySelectorAll('#tabla-body tr');

    // Iterar sobre cada fila y marcar o desmarcar el checkbox correspondiente
    rows.forEach(function(row) {
        // Verificar si la fila está visible
        if (row.style.display !== 'none') {
            // Obtener el checkbox de la fila actual
            var checkbox = row.querySelector('input[type="checkbox"]');
            // Marcar o desmarcar el checkbox según el estado del botón "Select All"
            checkbox.checked = isChecked;
        }
    });
});
