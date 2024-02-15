function cargarTabla() {
    // Obtener el valor seleccionado del menú desplegable
    var usuarioSeleccionado = document.getElementById('usuariosDropdown').value;

    // Enviar la solicitud a Flask para obtener los resultados en base al usuario seleccionado
    fetch('/obtener_torneos_jugador/' + encodeURIComponent(usuarioSeleccionado))
        .then(response => response.json())
        .then(data => {
            // Actualizar la tabla con los resultados
            actualizarTabla(data);
        })
        .catch(error => {
            console.error('Error al obtener resultados:', error);
        });
}

function actualizarTabla(data) {
    // Limpiar la tabla existente
    var tabla = document.getElementById('tablaTorneos');
    tabla.innerHTML = '';

    // Orden específico de las columnas
    var columnas = ['fecha_ano', 'fecha_str', 'nombre_torneo', 'lugar', 'categoria', 'total_partidos_jugados', 'partidos_ganados', 'finales_jugadas', 'finales_ganadas'];

    // Mapear las columnas a nombres deseados
    var nombresColumnas = {
        'fecha_ano': 'Año',
        'fecha_str': 'Fecha',
        'nombre_torneo': 'Nombre del Torneo',
        'lugar': 'Lugar',
        'categoria': 'Categoría',
        'total_partidos_jugados': 'Total Partidos Jugados',
        'partidos_ganados': 'Partidos Ganados',
        'finales_jugadas': 'Finales Jugadas',
        'finales_ganadas': 'Finales Ganadas'
    };

    // Crear encabezados de tabla
    var encabezadoRow = tabla.insertRow();
    columnas.forEach(encabezado => {
        var cell = encabezadoRow.insertCell();
        cell.textContent = nombresColumnas[encabezado] || encabezado;
    });

    // Crear filas de datos
    var maxFilas = Math.max(...columnas.map(encabezado => data[encabezado].length));
    for (var i = 0; i < maxFilas; i++) {
        var dataRow = tabla.insertRow();
        columnas.forEach(encabezado => {
            var cell = dataRow.insertCell();
            cell.textContent = data[encabezado][i] || ''; // Asegurar que no sea undefined
        });
    }
}

// Llamada inicial para cargar el menú desplegable
document.addEventListener('DOMContentLoaded', function() {
    cargarMenuDesplegable();
});

function cargarMenuDesplegable() {
    // Enviar la solicitud a Flask para obtener la lista de usuarios
    fetch('/obtener_lista_jugadores')
        .then(response => response.json())
        .then(data => {
            // Actualizar el menú desplegable con la lista de usuarios
            actualizarMenuDesplegable(data);
        })
        .catch(error => {
            console.error('Error al obtener usuarios:', error);
        });
}

function actualizarMenuDesplegable(data) {
    // Obtener el menú desplegable
    var dropdown = document.getElementById('usuariosDropdown');

    // Limpiar opciones existentes
    dropdown.innerHTML = '';

    var option = document.createElement('option');
        option.value = 0;  // Asignar el ID como el valor de la opción
        option.textContent = '';  // Mostrar el nombre del usuario
        dropdown.appendChild(option);

    // Agregar nuevas opciones al menú desplegable
    data.forEach(usuario => {
        var option = document.createElement('option');
        option.value = usuario.id_jugador_unico;  // Asignar el ID como el valor de la opción
        option.textContent = usuario.nombre_jugador;  // Mostrar el nombre del usuario
        dropdown.appendChild(option);
    });

}
