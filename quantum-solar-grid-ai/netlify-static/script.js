// script.js

const maxPoints = 16;
const labels = [];
const solarData = [];
const consumptionData = [];

function createChart(ctx, label, borderColor, backgroundColor) {
    return new Chart(ctx, {
        type: 'line',
        data: {
            labels,
            datasets: [{
                label,
                data: [],
                borderColor,
                backgroundColor,
                tension: 0.35,
                fill: true,
                pointRadius: 0,
                borderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    grid: { color: 'rgba(255,255,255,0.08)' },
                    ticks: { color: 'rgba(255,255,255,0.7)', maxRotation: 0, autoSkip: true, maxTicksLimit: 6 }
                },
                y: {
                    grid: { color: 'rgba(255,255,255,0.08)' },
                    ticks: { color: 'rgba(255,255,255,0.7)' }
                }
            },
            plugins: {
                legend: { display: false }
            }
        }
    });
}

const solarChart = createChart(
    document.getElementById('solarChart').getContext('2d'),
    'Solar generation (kWh)',
    'rgba(106, 236, 172, 1)',
    'rgba(106, 236, 172, 0.25)'
);

const consumptionChart = createChart(
    document.getElementById('consumptionChart').getContext('2d'),
    'Home consumption (kWh)',
    'rgba(255, 222, 87, 1)',
    'rgba(255, 222, 87, 0.25)'
);

function addDataPoint(solar, consumption) {
    const now = new Date();
    const label = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

    if (labels.length >= maxPoints) {
        labels.shift();
        solarData.shift();
        consumptionData.shift();
    }

    labels.push(label);
    solarData.push(solar);
    consumptionData.push(consumption);

    solarChart.data.datasets[0].data = solarData;
    consumptionChart.data.datasets[0].data = consumptionData;

    solarChart.update('none');
    consumptionChart.update('none');
}

function updateUI(data) {
    document.getElementById('solar-generation').textContent = data.solar_generation.toFixed(2);
    document.getElementById('consumption').textContent = data.consumption.toFixed(2);
    document.getElementById('battery-level').textContent = data.battery_level.toFixed(1);
    document.getElementById('grid-price').textContent = data.grid_price.toFixed(2);
    document.getElementById('decision').textContent = data.decision;

    // Update weather data
    if (data.weather) {
        document.getElementById('temperature').textContent = data.weather.temperature.toFixed(1);
        document.getElementById('weather-condition').textContent = data.weather.condition;
        document.getElementById('weather-description').textContent = data.weather.description;
    }

    addDataPoint(data.solar_generation, data.consumption);
}

const API_BASE = 'http://localhost:5000';

function fetchOptimization() {
    fetch(`${API_BASE}/api/run-optimization`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(updateUI)
        .catch(error => {
            console.error('Error fetching data:', error);
            alert('Error running optimization. Please ensure the Flask server is running on http://localhost:5000 and reload this page there.');
        });
}

document.getElementById('run-optimization').addEventListener('click', fetchOptimization);

// Run once on load to populate, then refresh every minute
fetchOptimization();
setInterval(fetchOptimization, 60_000);