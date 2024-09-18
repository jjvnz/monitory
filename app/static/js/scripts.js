document.addEventListener("DOMContentLoaded", function() {
    // Verifica la existencia de los elementos antes de continuar
    const cpuCtx = document.getElementById('cpuChart')?.getContext('2d');
    const memoryCtx = document.getElementById('memoryChart')?.getContext('2d');
    const diskCtx = document.getElementById('diskChart')?.getContext('2d');
    const historicalCtx = document.getElementById('historicalChart')?.getContext('2d');

    if (!cpuCtx || !memoryCtx || !diskCtx || !historicalCtx) {
        console.error('Faltan elementos de gráficos en el DOM.');
        return;
    }

    const maxDataPoints = 50; // Número máximo de puntos en los gráficos

    function trimData(chart) {
        if (chart.data.labels.length > maxDataPoints) {
            chart.data.labels.shift();
            chart.data.datasets.forEach(dataset => dataset.data.shift());
        }
    }

    const cpuChart = new Chart(cpuCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Uso de CPU (%)',
                data: [],
                borderColor: 'rgb(75, 192, 192)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)'
            }]
        }
    });

    const memoryChart = new Chart(memoryCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Uso de Memoria (%)',
                data: [],
                borderColor: 'rgb(153, 102, 255)',
                backgroundColor: 'rgba(153, 102, 255, 0.2)'
            }]
        }
    });

    const diskChart = new Chart(diskCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Uso de Disco (%)',
                data: [],
                borderColor: 'rgb(255, 159, 64)',
                backgroundColor: 'rgba(255, 159, 64, 0.2)'
            }]
        }
    });

    const historicalChart = new Chart(historicalCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'CPU (%)',
                    data: [],
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)'
                },
                {
                    label: 'Memoria (%)',
                    data: [],
                    borderColor: 'rgb(153, 102, 255)',
                    backgroundColor: 'rgba(153, 102, 255, 0.2)'
                },
                {
                    label: 'Disco (%)',
                    data: [],
                    borderColor: 'rgb(255, 159, 64)',
                    backgroundColor: 'rgba(255, 159, 64, 0.2)'
                }
            ]
        }
    });

    function updateCharts() {
        fetch('/metrics')
            .then(response => response.json())
            .then(data => {
                const now = new Date().toLocaleTimeString();

                if (document.getElementById('showCpu')?.checked) {
                    cpuChart.data.labels.push(now);
                    cpuChart.data.datasets[0].data.push(data.cpu_percent);
                    trimData(cpuChart);
                    cpuChart.update();
                }

                if (document.getElementById('showMemory')?.checked) {
                    memoryChart.data.labels.push(now);
                    memoryChart.data.datasets[0].data.push(data.memory_percent);
                    trimData(memoryChart);
                    memoryChart.update();
                }

                if (document.getElementById('showDisk')?.checked) {
                    diskChart.data.labels.push(now);
                    diskChart.data.datasets[0].data.push(data.disk_percent);
                    trimData(diskChart);
                    diskChart.update();
                }
            })
            .catch(error => {
                console.error('Error fetching metrics:', error);
                Swal.fire({
                    title: 'Error',
                    text: 'No se pudo actualizar los gráficos.',
                    icon: 'error'
                });
            });
    }

    function updateHistoricalChart() {
        fetch('/historical_data')
            .then(response => response.json())
            .then(data => {
                const labels = data.map(row => row[0]); // Timestamps
                const cpuData = data.map(row => row[1]); // CPU percentages
                const memoryData = data.map(row => row[2]); // Memory percentages
                const diskData = data.map(row => row[3]); // Disk percentages

                historicalChart.data.labels = labels;
                historicalChart.data.datasets[0].data = cpuData;
                historicalChart.data.datasets[1].data = memoryData;
                historicalChart.data.datasets[2].data = diskData;
                historicalChart.update();
            })
            .catch(error => {
                console.error('Error fetching historical data:', error);
                Swal.fire({
                    title: 'Error',
                    text: 'No se pudo actualizar el gráfico histórico.',
                    icon: 'error'
                });
            });
    }

    function handleAlertSettings(event) {
        event.preventDefault();
        const cpuThreshold = parseInt(document.getElementById('cpuThreshold')?.value) || 80;
        const memoryThreshold = parseInt(document.getElementById('memoryThreshold')?.value) || 85;
        const diskThreshold = parseInt(document.getElementById('diskThreshold')?.value) || 90;

        fetch(`/suggestions?cpu=${cpuThreshold}&memory=${memoryThreshold}&disk=${diskThreshold}`)
            .then(response => response.json())
            .then(data => {
                if (data.suggestions.length > 0) {
                    Swal.fire({
                        title: 'Sugerencias de Alertas',
                        text: data.suggestions.join('\n'),
                        icon: 'warning'
                    });
                } else {
                    Swal.fire({
                        title: 'Todo está bien',
                        text: 'No se han detectado problemas.',
                        icon: 'success'
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching suggestions:', error);
                Swal.fire({
                    title: 'Error',
                    text: 'No se pudieron obtener las sugerencias.',
                    icon: 'error'
                });
            });
    }

    const alertsForm = document.getElementById('alertsForm');
    if (alertsForm) {
        alertsForm.addEventListener('submit', handleAlertSettings);
    } else {
        console.error('El formulario de alertas no se encuentra en el DOM.');
    }

    // Configurar intervalos para actualizar los gráficos
    updateCharts();
    setInterval(updateCharts, 5000); // Actualizar cada 5 segundos
    updateHistoricalChart();
});
