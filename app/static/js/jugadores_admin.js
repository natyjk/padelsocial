var nombresSeleccionadosIzquierda = [];
var nombreSeleccionadoDerecha = null;
// Función para manejar la selección de nombres
function seleccionarNombre(event) {

    const nombreSeleccionado = event.target.textContent;

    // Alternar la selección del nombre
    if (nombreSeleccionado) {
        const index = nombresSeleccionadosIzquierda.indexOf(nombreSeleccionado);
        if (index === -1) {
            nombresSeleccionadosIzquierda.push(nombreSeleccionado);
            event.target.classList.add('seleccionado');
        } else {
            nombresSeleccionadosIzquierda.splice(index, 1);
            event.target.classList.remove('seleccionado');
        }
    }
}

function seleccionarUnicoNombre(event) {
    const nombreSeleccionado = event.target.textContent;

    // Seleccionar solo un nombre en la lista derecha
    nombreSeleccionadoDerecha = nombreSeleccionado;

    // Desmarcar todos los elementos en la lista derecha
    Array.from(document.getElementById('listaDerecha').children).forEach(item => {
        item.classList.remove('seleccionado');
    });

    // Marcar el nombre seleccionado en la lista derecha
    if (nombreSeleccionado) {
        event.target.classList.add('seleccionado');
    }
}

// Función para agrupar nombres (puedes ajustar esta función según tus necesidades)
function agruparNombres() {

    // Verificar que haya al menos un nombre seleccionado en la lista izquierda
    if (nombresSeleccionadosIzquierda.length === 0) {
        alert('Selecciona al menos un nombre en la lista izquierda.');
        return;
    }

    // Verificar que haya solo un nombre seleccionado en la lista derecha
    if (!nombreSeleccionadoDerecha) {
        alert('Debes seleccionar un nombre en la lista derecha, si no encuentras opciones, crea un nuevo jugador.');
        // Cambiar la clase del botón
        const btnNuevoJugador = document.getElementById('btnNuevoJugador');
        btnNuevoJugador.classList.remove('btn-outline-success'); // Elimina la clase actual
        btnNuevoJugador.classList.add('btn-success'); // Agrega la nueva clase

        return;
    }

    // Enviar las variables al servidor o realizar la acción deseada
    console.log('Nombres Izquierda:', nombresSeleccionadosIzquierda);
    console.log('Nombre Derecha:', nombreSeleccionadoDerecha);

    // Convertir la lista de nombres izquierda a cadena JSON
    const nombresIzquierdaJSON = JSON.stringify(nombresSeleccionadosIzquierda);

    // Hacer una solicitud al servidor para ejecutar la función de Python
    fetch('/agrupar_jugadores/' , {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
        nombresIzquierda: nombresIzquierdaJSON,
        nombreDerecha: nombreSeleccionadoDerecha,
    }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
    })
    .catch(error => console.error('Error:', error));

    // Restablecer selecciones después de agrupar
    nombresSeleccionadosIzquierda = [];
    nombreSeleccionadoDerecha = null;

    // Restablecer estilos
    Array.from(document.getElementById('listaIzquierda').children).forEach(item => {
        item.classList.remove('seleccionado');
    });

    Array.from(document.getElementById('listaDerecha').children).forEach(item => {
        item.classList.remove('seleccionado');
    });
    document.getElementById('listaIzquierda').innerHTML = '';
    document.getElementById('listaDerecha').innerHTML = '';
    document.getElementById('inputBuscar').value = '';

    alert('Jugadores agrupados.');
}

function crearNuevoUsuario() {
    // Verificar que haya al menos un nombre seleccionado en la lista izquierda
    if (nombresSeleccionadosIzquierda.length === 0) {
        alert('Selecciona al menos un nombre en la lista izquierda.');
        return;
    }

    // Mostrar el área de creacion
    document.getElementById('areaActualizacion').style.display = 'block';
    // Cambiar la clase del botón
    const btnNuevoJugador = document.getElementById('btnNuevoJugador');
    btnNuevoJugador.classList.remove('btn-success'); // Elimina la clase actual
    btnNuevoJugador.classList.add('btn-outline-success'); // Agrega la nueva clase

    // Ocultar el área de agrupacion
    document.getElementById('areaAgrupacion').style.display = 'none';

}

function borrarFiltros() {
    document.getElementById('listaIzquierda').innerHTML = '';
    document.getElementById('listaDerecha').innerHTML = '';
    document.getElementById('inputBuscar').value = '';
}

function buscarNombres() {
    console.log('Aquí entro')   ;

    var nombresDisponibles = '';
    var nombresUnicosDisponibles = '';

    var inputBuscar = document.getElementById('inputBuscar');
    var textoBuscado = inputBuscar.value.toLowerCase();
    console.log(textoBuscado)

    fetch('/cargar_nombres/'  + encodeURIComponent(textoBuscado) , {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        // Si la respuesta no es un JSON, retornar la respuesta completa
        if (response.headers.get('content-type').toLowerCase() !== 'application/json') {
            return response.text();
        }
        return response.json();
    })
    .then(data => {
        var nombresDisponibles = data.jugadores_all.map(function(obj) {
            return obj.nombre_jugador;
        });

        var nombresUnicosDisponibles = data.jugadores_unicos.map(function(obj) {
            return obj.nombre_completo;
        });

        const listaIzquierda = document.getElementById('listaIzquierda');
        const fragmento = document.createDocumentFragment();

        nombresDisponibles.forEach(nombre => {
            const listItem = document.createElement('li');
            listItem.textContent = nombre;
            listItem.classList.add('list-group-item');
            // Agregar evento de clic para seleccionar/deseleccionar nombres
            listItem.addEventListener('click', function(event) {
                seleccionarNombre(event);
            });

            fragmento.appendChild(listItem);
        });

        listaIzquierda.appendChild(fragmento);


        const listaDerecha = document.getElementById('listaDerecha');
        const fragmento2 = document.createDocumentFragment();

        nombresUnicosDisponibles.forEach(nombre => {
            const listItem = document.createElement('li');
            listItem.textContent = nombre;
            listItem.classList.add('list-group-item');
            // Agregar evento de clic para seleccionar/deseleccionar nombres únicos
            listItem.addEventListener('click', function(event) {
                seleccionarUnicoNombre(event);
            });
            fragmento2.appendChild(listItem);
        });

        listaDerecha.appendChild(fragmento2);

        var nombresDisponibles = '';
        var nombresUnicosDisponibles = '';

    })
    .catch(error => console.error('Error:', error));
}

function crearJugador() {

    const nombreInput = document.getElementById('nombreInput').value;
    const apellidoInput = document.getElementById('apellidoInput').value;
    // Convertir la lista de nombres izquierda a cadena JSON
    //const nombresIzquierdaJSON = JSON.stringify(nombresSeleccionadosIzquierda);

    var data = {
        nombresIzquierda: nombresSeleccionadosIzquierda,
        nombre: nombreInput,
        apellido: apellidoInput
    };

    // Convertir el objeto JSON a una cadena JSON
    var jsonData = JSON.stringify(data);

    console.log(jsonData)

    // Hacer una solicitud al servidor para ejecutar la función de Python
    fetch('/crear_nuevo_jugador/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: jsonData,
    })
    .then(response => response.json())
    .then(data => {
        // Manejar la respuesta del servidor si es necesario
        console.log(data);
    })
        .catch(error => console.error('Error:', error));


    // Limpiar los campos de entrada después de la actualización
    document.getElementById('nombreInput').value = '';
    document.getElementById('apellidoInput').value = '';
    document.getElementById('inputBuscar').value = '';
    document.getElementById('listaIzquierda').innerHTML = '';
    document.getElementById('listaDerecha').innerHTML = '';

    // NO Mostrar el área de creacion
    document.getElementById('areaActualizacion').style.display = 'none';
    // Cambiar la clase del botón
    const btnNuevoJugador = document.getElementById('btnNuevoJugador');
    btnNuevoJugador.classList.remove('btn-success'); // Elimina la clase actual
    btnNuevoJugador.classList.add('btn-outline-success'); // Agrega la nueva clase

    // Mostrar área de agrupacion
    document.getElementById('areaAgrupacion').style.display = 'block';
}
