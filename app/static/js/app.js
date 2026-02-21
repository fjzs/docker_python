// Frontend JavaScript for the facility location optimization application

// Configuration
const GRID_SIZE = 100; // 100x100 unit grid
const CANVAS_SIZE = 500; // Canvas size in pixels
const SCALE = CANVAS_SIZE / GRID_SIZE; // Pixels per grid unit

// Get DOM elements
const generateForm = document.getElementById('generateForm');
const resultContainer = document.getElementById('resultContainer');
const resultData = document.getElementById('resultData');
const gridCanvas = document.getElementById('gridCanvas');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');

// Form submission handler
generateForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Clear previous errors
    errorContainer.style.display = 'none';

    // Get form values
    const nCustomers = parseInt(document.getElementById('n_customers').value);
    const nFacilities = parseInt(document.getElementById('n_facilities').value);

    try {
        // Call API
        const response = await fetch('/api/generate-instance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                n_customers: nCustomers,
                n_facilities: nFacilities,
            }),
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const instance = await response.json();

        // Display results
        displayResults(instance);

    } catch (error) {
        showError(`Error generating instance: ${error.message}`);
    }
});

/**
 * Display the generated instance data and visualization
 */
function displayResults(instance) {
    // Display JSON data
    const dataStr = JSON.stringify(instance, null, 2);
    resultData.innerHTML = `<pre>${escapeHtml(dataStr)}</pre>`;

    // Draw on canvas
    drawGrid(instance);

    // Show result container
    resultContainer.style.display = 'block';
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Draw the grid with customers and facilities
 */
function drawGrid(instance) {
    const ctx = gridCanvas.getContext('2d');

    // Clear canvas
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

    // Draw grid lines (light gray)
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= GRID_SIZE; i += 10) {
        const pixel = i * SCALE;
        // Vertical lines
        ctx.beginPath();
        ctx.moveTo(pixel, 0);
        ctx.lineTo(pixel, CANVAS_SIZE);
        ctx.stroke();
        // Horizontal lines
        ctx.beginPath();
        ctx.moveTo(0, pixel);
        ctx.lineTo(CANVAS_SIZE, pixel);
        ctx.stroke();
    }

    // Draw grid border
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.strokeRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

    // Draw customers (blue circles)
    ctx.fillStyle = '#3b82f6';
    instance.customers.forEach((customer) => {
        const x = customer.x * SCALE;
        const y = customer.y * SCALE;
        ctx.beginPath();
        ctx.arc(x, y, 4, 0, 2 * Math.PI);
        ctx.fill();
    });

    // Draw facilities (red squares)
    ctx.fillStyle = '#ef4444';
    instance.facilities.forEach((facility) => {
        const x = facility.x * SCALE;
        const y = facility.y * SCALE;
        ctx.fillRect(x - 4, y - 4, 8, 8);
    });

    // Draw legend
    drawLegend(ctx, instance);
}

/**
 * Draw legend on canvas
 */
function drawLegend(ctx, instance) {
    const legendX = 10;
    const legendY = CANVAS_SIZE - 50;
    const legendSpacing = 60;

    // Background
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fillRect(legendX - 5, legendY - 5, 150, 50);
    ctx.strokeStyle = '#999';
    ctx.lineWidth = 1;
    ctx.strokeRect(legendX - 5, legendY - 5, 150, 50);

    // Customer marker
    ctx.fillStyle = '#3b82f6';
    ctx.beginPath();
    ctx.arc(legendX + 10, legendY + 10, 4, 0, 2 * Math.PI);
    ctx.fill();

    ctx.fillStyle = '#333';
    ctx.font = '12px sans-serif';
    ctx.textAlign = 'left';
    ctx.fillText('Customers', legendX + 20, legendY + 15);

    // Facility marker
    ctx.fillStyle = '#ef4444';
    ctx.fillRect(legendX + 10 + legendSpacing - 4, legendY + 10 - 4, 8, 8);

    ctx.fillStyle = '#333';
    ctx.fillText('Facilities', legendX + 20 + legendSpacing, legendY + 15);
}

/**
 * Show error message
 */
function showError(message) {
    errorMessage.textContent = message;
    errorContainer.style.display = 'block';
}

/**
 * Escape HTML special characters
 */
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;',
    };
    return text.replace(/[&<>"']/g, (m) => map[m]);
}

