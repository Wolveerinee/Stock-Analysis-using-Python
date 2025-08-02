// Stock Chart Management
let stockChart = null;
let currentChartType = 'price';

/**
 * Initialize the stock chart with price data
 */
function initializeStockChart() {
    if (!window.chartData || !window.stockSymbol) {
        console.error('Chart data not available');
        return;
    }

    const ctx = document.getElementById('stockChart');
    if (!ctx) {
        console.error('Chart canvas not found');
        return;
    }

    // Destroy existing chart if it exists
    if (stockChart) {
        stockChart.destroy();
    }

    // Create the chart
    stockChart = new Chart(ctx, {
        type: 'line',
        data: getPriceChartData(),
        options: getChartOptions('price')
    });
}

/**
 * Update chart type (price or volume)
 */
function updateChartType(type) {
    if (!stockChart || !window.chartData) {
        return;
    }

    currentChartType = type;
    
    // Update chart data and options
    if (type === 'price') {
        stockChart.data = getPriceChartData();
        stockChart.options = getChartOptions('price');
    } else if (type === 'volume') {
        stockChart.data = getVolumeChartData();
        stockChart.options = getChartOptions('volume');
    }
    
    stockChart.update('active');
}

/**
 * Get price chart data configuration
 */
function getPriceChartData() {
    return {
        labels: window.chartData.labels,
        datasets: [
            {
                label: `${window.stockSymbol} Close Price`,
                data: window.chartData.prices,
                borderColor: '#58a6ff',
                backgroundColor: 'rgba(88, 166, 255, 0.1)',
                borderWidth: 2,
                fill: true,
                tension: 0.1,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: '#58a6ff',
                pointHoverBorderColor: '#ffffff',
                pointHoverBorderWidth: 2
            },
            {
                label: `${window.stockSymbol} High`,
                data: window.chartData.highs,
                borderColor: '#3fb950',
                backgroundColor: 'rgba(63, 185, 80, 0.05)',
                borderWidth: 1,
                fill: false,
                tension: 0.1,
                pointRadius: 0,
                pointHoverRadius: 4,
                borderDash: [5, 5]
            },
            {
                label: `${window.stockSymbol} Low`,
                data: window.chartData.lows,
                borderColor: '#f85149',
                backgroundColor: 'rgba(248, 81, 73, 0.05)',
                borderWidth: 1,
                fill: false,
                tension: 0.1,
                pointRadius: 0,
                pointHoverRadius: 4,
                borderDash: [5, 5]
            }
        ]
    };
}

/**
 * Get volume chart data configuration
 */
function getVolumeChartData() {
    return {
        labels: window.chartData.labels,
        datasets: [
            {
                label: `${window.stockSymbol} Volume`,
                data: window.chartData.volumes,
                backgroundColor: 'rgba(88, 166, 255, 0.6)',
                borderColor: '#58a6ff',
                borderWidth: 1,
                type: 'bar'
            }
        ]
    };
}

/**
 * Get chart options based on chart type
 */
function getChartOptions(type) {
    const baseOptions = {
        responsive: true,
        maintainAspectRatio: false,
        interaction: {
            intersect: false,
            mode: 'index'
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    color: '#e6edf3',
                    usePointStyle: true,
                    padding: 20,
                    font: {
                        size: 12,
                        family: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans", Helvetica, Arial, sans-serif'
                    }
                }
            },
            tooltip: {
                backgroundColor: 'rgba(13, 17, 23, 0.95)',
                titleColor: '#e6edf3',
                bodyColor: '#e6edf3',
                borderColor: '#30363d',
                borderWidth: 1,
                cornerRadius: 8,
                padding: 12,
                displayColors: true,
                callbacks: {
                    label: function(context) {
                        if (type === 'price') {
                            return `${context.dataset.label}: $${context.parsed.y.toFixed(2)}`;
                        } else if (type === 'volume') {
                            return `${context.dataset.label}: ${context.parsed.y.toLocaleString()}`;
                        }
                    }
                }
            }
        },
        scales: {
            x: {
                display: true,
                title: {
                    display: true,
                    text: 'Date',
                    color: '#e6edf3',
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                },
                ticks: {
                    color: '#8b949e',
                    maxTicksLimit: 10,
                    callback: function(value, index, values) {
                        const date = new Date(this.getLabelForValue(value));
                        return date.toLocaleDateString('en-US', { 
                            month: 'short', 
                            day: 'numeric' 
                        });
                    }
                },
                grid: {
                    color: 'rgba(230, 237, 243, 0.1)',
                    borderColor: '#30363d'
                }
            },
            y: {
                display: true,
                title: {
                    display: true,
                    text: type === 'price' ? 'Price ($)' : 'Volume',
                    color: '#e6edf3',
                    font: {
                        size: 14,
                        weight: 'bold'
                    }
                },
                ticks: {
                    color: '#8b949e',
                    callback: function(value, index, values) {
                        if (type === 'price') {
                            return '$' + value.toFixed(2);
                        } else if (type === 'volume') {
                            return value.toLocaleString();
                        }
                    }
                },
                grid: {
                    color: 'rgba(230, 237, 243, 0.1)',
                    borderColor: '#30363d'
                }
            }
        }
    };

    // Add zoom and pan capabilities
    baseOptions.plugins.zoom = {
        zoom: {
            wheel: {
                enabled: true,
            },
            pinch: {
                enabled: true
            },
            mode: 'x',
        },
        pan: {
            enabled: true,
            mode: 'x',
        }
    };

    return baseOptions;
}

/**
 * Format large numbers for display
 */
function formatLargeNumber(num) {
    if (num >= 1e12) {
        return (num / 1e12).toFixed(1) + 'T';
    } else if (num >= 1e9) {
        return (num / 1e9).toFixed(1) + 'B';
    } else if (num >= 1e6) {
        return (num / 1e6).toFixed(1) + 'M';
    } else if (num >= 1e3) {
        return (num / 1e3).toFixed(1) + 'K';
    } else {
        return num.toString();
    }
}

/**
 * Add loading animation to chart
 */
function showChartLoading() {
    const chartContainer = document.getElementById('stockChart').parentElement;
    chartContainer.classList.add('loading');
}

/**
 * Remove loading animation from chart
 */
function hideChartLoading() {
    const chartContainer = document.getElementById('stockChart').parentElement;
    chartContainer.classList.remove('loading');
}

/**
 * Handle chart resize
 */
function handleChartResize() {
    if (stockChart) {
        stockChart.resize();
    }
}

// Add event listeners
window.addEventListener('resize', handleChartResize);

// Export functions for global use
window.initializeStockChart = initializeStockChart;
window.updateChartType = updateChartType;
window.showChartLoading = showChartLoading;
window.hideChartLoading = hideChartLoading;
