document.getElementById('consultaForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const calcio = parseFloat(document.getElementById('calcio').value) || 0;  // Valor padrão
    const ureia = parseFloat(document.getElementById('ureia').value) || 0;
    const ph = parseFloat(document.getElementById('ph').value) || 7;
    const condutividade = parseFloat(document.getElementById('condutividade').value) || 0;
    const gravidade = parseFloat(document.getElementById('gravidade').value) || 0;
    const osmolaridade = parseFloat(document.getElementById('osmolaridade').value) || 0;

    fetch('http://127.0.0.1:5000/consultamodelo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            calcio: calcio,
            ureia: ureia,
            pH: ph,
            condutividade: condutividade,
            gravidade: gravidade,
            osmolaridade: osmolaridade
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Erro na rede');
        }
        return response.json();
    })
    .then(data => {
        document.getElementById('resultado').textContent = data.resultado;
    })
    .catch(error => {
        console.error('Erro:', error);
        document.getElementById('resultado').textContent = "Erro ao consultar o backend.";
    });
});

