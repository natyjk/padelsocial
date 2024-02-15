// Obtener referencia al dropdown de usuarios
const dropdownUsuarios = document.getElementById('dropdown-usuarios');


// Función para cargar los nombres de usuarios desde el servidor al cargar la página
function cargarNombresUsuarios() {
    // Realizar una solicitud AJAX para obtener los nombres de usuarios desde el servidor
    fetch('/obtener_lista_jugadores')
        .then(response => response.json())
        .then(data => {
            // Actualizar el menú desplegable con la lista de usuarios
            actualizarMenuDesplegable(data);
        })
        .catch(error => {
            console.error('Error al cargar jugadores:', error);
        });
}

function actualizarMenuDesplegable(data) {
    // Obtener el menú desplegable
    var dropdown = document.getElementById('dropdown-usuarios');

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
        option.textContent = usuario.nombre_completo;  // Mostrar el nombre del usuario
        dropdown.appendChild(option);
    });

}

// Llamar a la función de cargar nombres de usuarios al cargar la página
window.addEventListener('load', cargarNombresUsuarios);

const tablaResumen = document.getElementById('tabla-resumen');


// Función para cargar los datos del usuario seleccionado
function cargarDatosUsuario() {
    // Obtener el valor seleccionado en el dropdown de usuarios
    var usuarioSeleccionado = document.getElementById('dropdown-usuarios').value;

    console.log('Aqui voy!');
    console.log(usuarioSeleccionado);

    // Realizar una solicitud AJAX para cargar los datos del usuario
    fetch('/cargar_datos_usuario/'+ encodeURIComponent(usuarioSeleccionado))
    .then(response => response.json())
    .then(data => {
        // Actualizar la tabla de resumen con los datos del usuario
        actualizarTablaResumen(data);
        actualizarTituloJugador(data['nombre'] + ' ' + data['apellido']);
        cargarGraficos(usuarioSeleccionado);
        cargarTabla()
        document.getElementById("contenidoOculto").style.display = "block";
    })
    .catch(error => {
        console.error('Error al cargar los datos del usuario:', error);
    });
}

// Función para actualizar la tabla de resumen con los datos del usuario
function actualizarTablaResumen(datosUsuario) {

    console.log(datosUsuario)
    // Limpiar la tabla antes de actualizar los datos
    var tablaResumen = document.getElementById('tablaResumen');
    tablaResumen.innerHTML = '';


    // Orden específico de las columnas
    var columnas = ['torneos_jugados', 'finales_ganadas', 'p_torneos_ganados', 'finales_jugadas', 'p_finales', 'total_partidos_jugados', 'p_partidos_ganados'];

    // Mapear las columnas a nombres deseados
    var nombresColumnas = {
        'torneos_jugados': 'Total torneos jugados',
        'finales_ganadas': 'Total torneos ganados',
        'p_torneos_ganados': '% Torneos ganados',
        'finales_jugadas': 'Total finales jugadas',
        'p_finales': '% Torneos final jugada',
        'total_partidos_jugados': 'Total partidos jugados',
        'p_partidos_ganados': '% Partidos ganados'
    };

    // Crear encabezados de tabla
    var encabezadoRow = tablaResumen.insertRow();
    columnas.forEach(encabezado => {
        var cell = encabezadoRow.insertCell();
        cell.textContent = nombresColumnas[encabezado] || encabezado;
    });

    // Crear la fila de datos
    var datosRow = tablaResumen.insertRow();
    columnas.forEach(columna => {
        var cell = datosRow.insertCell();
        var valor = datosUsuario[columna];
        // Formatear el valor si es un porcentaje
        if (columna.startsWith('p_')) {
            valor = (parseFloat(valor) * 100).toFixed(0) + '%';
        }
        cell.textContent = valor;
    });
}

// Función para actualizar el título con el nombre del jugador seleccionado
function actualizarTituloJugador(nombreJugador) {
    var tituloJugador = document.getElementById('tituloJugador');
    if (tituloJugador) {
        tituloJugador.textContent = nombreJugador;
    }
}

function cargarGraficos(usuarioSeleccionado) {

    // Limpiar los contenedores de los gráficos
    document.getElementById('grafico1').innerHTML = '';
    document.getElementById('grafico2').innerHTML = '';
    document.getElementById('grafico3').innerHTML = '';
    document.getElementById('grafico4').innerHTML = '';

    fetch('/grafico/'+ encodeURIComponent(usuarioSeleccionado))
    .then(response => response.json())
    .then(data => {
        // Procesar las imágenes Base64 y mostrarlas en tu aplicación web
        var img1 = document.createElement('img');
        img1.src = 'data:image/png;base64,' + data.graph1;
        document.getElementById('grafico1').appendChild(img1);

        var img2 = document.createElement('img');
        img2.src = 'data:image/png;base64,' + data.graph2;
        document.getElementById('grafico2').appendChild(img2);

        var img3 = document.createElement('img');
        img3.src = 'data:image/png;base64,' + data.graph3;
        document.getElementById('grafico3').appendChild(img3);

        var img4 = document.createElement('img');
        img4.src = 'data:image/png;base64,' + data.graph4;
        document.getElementById('grafico4').appendChild(img4);
    })
    .catch(error => {
        console.error('Error al cargar los gráficos:', error);
    });
}

// Evento para cargar los datos del usuario al seleccionar uno del dropdown
dropdownUsuarios.addEventListener('change', cargarDatosUsuario);

// Llamar a la función de cargar los datos del usuario al cargar la página (opcional)
//window.addEventListener('load', cargarDatosUsuario);

function cargarTabla() {
    // Obtener el valor seleccionado del menú desplegable
    var usuarioSeleccionado = document.getElementById('dropdown-usuarios').value;

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
    var columnas = ['fecha_ano', 'fecha_str', 'nombre_torneo', 'lugar', 'categoria', 'pareja', 'total_partidos_jugados', 'partidos_ganados', 'finales_jugadas', 'finales_ganadas'];

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