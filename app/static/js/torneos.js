document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.extraer-data-torneo').forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            var torneoId = this.getAttribute('data-id');
            extraerDataTorneo(torneoId);
        });
    });
});

function extraerDataTorneo(torneoId) {
    fetch('/extraer_data_torneo/' + encodeURIComponent(torneoId), {
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
        // Hacer algo con la respuesta de la función Python
        console.log(data);
    })
    .catch(error => console.error('Error:', error));
}

function actualizarJugadores() {
        // Hacer una solicitud al servidor para ejecutar la función de Python
        fetch('/actualizar_jugadores', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Manejar la respuesta del servidor si es necesario
            console.log(data);
        })
        .catch(error => console.error('Error:', error));
    }