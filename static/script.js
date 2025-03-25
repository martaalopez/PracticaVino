document.getElementById('wineForm').addEventListener('submit', function (e) {
    e.preventDefault();

    // Crear un objeto FormData con los valores del formulario
    const formData = new FormData(this);

    // Enviar los datos al servidor Flask
    fetch('http://127.0.0.1:5000', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json()) // Asegúrate de que la respuesta sea JSON
        .then(data => {
            // Verificar si hubo un error en la respuesta
            if (data.error) {
                // Mostrar el error si existe
                const resultElement = document.getElementById('result');
                if (resultElement) {
                    resultElement.innerHTML = `Error: ${data.error}`;
                }
            } else {
                // Mostrar las predicciones
                const classificationElement = document.getElementById('classificationResult');
                const regressionElement = document.getElementById('regressionResult');

                if (classificationElement && regressionElement) {
                    classificationElement.innerHTML = `Clasificación: ${data.classification}`;
                    regressionElement.innerHTML = `Regresión: ${data.regression}`;
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            const resultElement = document.getElementById('result');
            if (resultElement) {
                resultElement.innerHTML = 'Hubo un error en la predicción.';
            }
        });
});

// Limpiar formulario
document.getElementById('clearForm').addEventListener('click', function () {
    var form = document.getElementById('wineForm');
    var inputs = form.querySelectorAll('input');

    inputs.forEach(function (input) {
        input.value = ''; // Limpiar el valor de cada campo
    });
});
