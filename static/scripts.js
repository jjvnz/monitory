// scripts.js

let cpuChart, memoryChart, diskChart;

function updateChart(chart, dataPoint) {
    chart.data.labels.push('');
    chart.data.datasets[0].data.push(dataPoint);
    if (chart.data.labels.length > 20) {
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    chart.update();
}

function updateProgressBar(id, value) {
    const progressBar = document.getElementById(id);
    const label = document.getElementById(id + 'Percentage');
    progressBar.style.width = value + '%';
    label.textContent = value + '%';
}

async function fetchMetrics() {
    const response = await fetch('/metrics');
    const data = await response.json();

    updateChart(cpuChart, data.cpu_percent);
    updateChart(memoryChart, data.memory_percent);
    updateChart(diskChart, data.disk_percent);

    updateProgressBar('cpuProgressBar', data.cpu_percent);
    updateProgressBar('memoryProgressBar', data.memory_percent);
    updateProgressBar('diskProgressBar', data.disk_percent);

    fetchSuggestions();
}

async function fetchSuggestions() {
    const response = await fetch('/suggestions');
    const data = await response.json();
    const suggestions = data.suggestions;

    if (suggestions.length > 0) {
        suggestions.forEach(suggestion => {
            Swal.fire({
                icon: 'warning',
                title: 'Sugerencia de Optimización',
                text: suggestion,
                confirmButtonText: 'Entendido',
                background: '#ffffff',
                customClass: {
                    title: 'text-lg text-gray-800',
                    confirmButton: 'bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded'
                }
            });
        });
    }
}

window.onload = function() {
    const ctxCpu = document.getElementById('cpuChart').getContext('2d');
    const ctxMemory = document.getElementById('memoryChart').getContext('2d');
    const ctxDisk = document.getElementById('diskChart').getContext('2d');

    cpuChart = new Chart(ctxCpu, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Uso de CPU (%)',
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                data: []
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, max: 100 }
            }
        }
    });

    memoryChart = new Chart(ctxMemory, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Uso de Memoria (%)',
                borderColor: 'rgb(153, 102, 255)',
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                data: []
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, max: 100 }
            }
        }
    });

    diskChart = new Chart(ctxDisk, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Uso de Disco (%)',
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                data: []
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true, max: 100 }
            }
        }
    });

    setInterval(fetchMetrics, 5000);  // Actualizar métricas y gráficos cada 5 segundos
}
