document.addEventListener('DOMContentLoaded', () => {
    const statusElement = document.getElementById('status');
    const dataView = document.getElementById('data-view');
    
    // Verificar conexión con el servidor
    checkServerStatus();
    
    // Obtener datos iniciales
    fetchData();
    
    // Actualizar datos cada 5 segundos
    setInterval(fetchData, 5000);
});

function checkServerStatus() {
    fetch('/')
        .then(response => {
            document.getElementById('status').textContent = 'Conectado al servidor';
            document.getElementById('status').className = 'status-connected';
        })
        .catch(error => {
            document.getElementById('status').textContent = 'Error de conexión';
            document.getElementById('status').className = 'status-error';
        });
}

function fetchData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('data-view').textContent = 
                JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
}