// Frontend JavaScript for the facility location optimization application

// Configuration
const GRID_SIZE = 100; // 100x100 unit grid
const CANVAS_SIZE = 500; // Canvas size in pixels
const SCALE = CANVAS_SIZE / GRID_SIZE; // Pixels per grid unit

// State
let currentInstance = null;
let currentSolution = null;

// Get DOM elements
const generateForm = document.getElementById('generateForm');
const solveButton = document.getElementById('solveButton');
const resultContainer = document.getElementById('resultContainer');
const resultData = document.getElementById('resultData');
const gridCanvas = document.getElementById('gridCanvas');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');

// ===============================
// GENERATE INSTANCE
// ===============================

generateForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    clearUI();
    hideError();

    const button = generateForm.querySelector('button');
    button.disabled = true;
    button.textContent = 'Generating...';

    const nCustomers = parseInt(document.getElementById('n_customers').value);
    const nFacilities = parseInt(document.getElementById('n_facilities').value);
    const openingCost = parseInt(document.getElementById('opening_cost').value);

    try {
        const response = await fetch('/api/generate-instance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                n_customers: nCustomers,
                n_facilities: nFacilities,
                opening_cost: openingCost,
            }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`${response.status}: ${errorText}`);
        }

        const instance = await response.json();

        currentInstance = instance;
        currentSolution = null;

        displayResults(instance);

        // Show solve button
        solveButton.style.display = 'inline-block';

    } catch (error) {
        showError(`Error generating instance: ${error.message}`);
    } finally {
        button.disabled = false;
        button.textContent = 'Generate Instance';
    }
});

// ===============================
// SOLVE INSTANCE
// ===============================

solveButton.addEventListener('click', async () => {
    if (!currentInstance) return;

    hideError();

    solveButton.disabled = true;
    solveButton.textContent = 'Solving...';

    try {
        const response = await fetch('/api/solve-instance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(currentInstance),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`${response.status}: ${errorText}`);
        }

        const solution = await response.json();
        currentSolution = solution;

        drawGrid(currentInstance, currentSolution);

    } catch (error) {
        showError(`Error solving instance: ${error.message}`);
    } finally {
        solveButton.disabled = false;
        solveButton.textContent = 'Solve Instance';
    }
});

// ===============================
// DISPLAY RESULTS
// ===============================

function displayResults(instance) {
    const dataStr = JSON.stringify(instance, null, 2);
    resultData.innerHTML = `<pre>${escapeHtml(dataStr)}</pre>`;

    drawGrid(instance);

    resultContainer.style.display = 'block';
    resultContainer.scrollIntoView({ behavior: 'smooth' });
}

// ===============================
// DRAW GRID
// ===============================

function drawGrid(instance, solution = null) {
    const ctx = gridCanvas.getContext('2d');

    // Clear canvas
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

    drawGridLines(ctx);

    // Draw assignments first (so nodes appear on top)
    if (solution) {
        drawAssignments(ctx, instance, solution);
    }

    drawCustomers(ctx, instance);
    drawFacilities(ctx, instance, solution);

    drawLegend(ctx);
}

function drawGridLines(ctx) {
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 0.5;

    for (let i = 0; i <= GRID_SIZE; i += 10) {
        const pixel = i * SCALE;

        ctx.beginPath();
        ctx.moveTo(pixel, 0);
        ctx.lineTo(pixel, CANVAS_SIZE);
        ctx.stroke();

        ctx.beginPath();
        ctx.moveTo(0, pixel);
        ctx.lineTo(CANVAS_SIZE, pixel);
        ctx.stroke();
    }

    ctx.strokeStyle = '#333';
    ctx.lineWidth = 2;
    ctx.strokeRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);
}

function drawCustomers(ctx, instance) {
    ctx.fillStyle = '#3b82f6';

    instance.customers.forEach((customer) => {
        const x = customer.x * SCALE;
        const y = customer.y * SCALE;

        ctx.beginPath();
        ctx.arc(x, y, 4, 0, 2 * Math.PI);
        ctx.fill();
    });
}

function drawFacilities(ctx, instance, solution) {
    instance.facilities.forEach((facility, index) => {
        const x = facility.x * SCALE;
        const y = facility.y * SCALE;

        const isOpen =
            solution && solution.open_facilities.includes(index);

        ctx.fillStyle = isOpen ? '#10b981' : '#ef4444';
        ctx.fillRect(x - 4, y - 4, 8, 8);
    });
}

function drawAssignments(ctx, instance, solution) {
    ctx.strokeStyle = '#999';
    ctx.lineWidth = 1;

    solution.assignments.forEach((assignment) => {
        const customer = instance.customers[assignment.customer_id];
        const facility = instance.facilities[assignment.facility_id];

        const cx = customer.x * SCALE;
        const cy = customer.y * SCALE;
        const fx = facility.x * SCALE;
        const fy = facility.y * SCALE;

        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(fx, fy);
        ctx.stroke();
    });
}

function drawLegend(ctx) {
    const legendX = 10;
    const legendY = CANVAS_SIZE - 50;

    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fillRect(legendX - 5, legendY - 5, 180, 50);

    ctx.strokeStyle = '#999';
    ctx.lineWidth = 1;
    ctx.strokeRect(legendX - 5, legendY - 5, 180, 50);

    ctx.font = '12px sans-serif';
    ctx.textAlign = 'left';

    // Customer
    ctx.fillStyle = '#3b82f6';
    ctx.beginPath();
    ctx.arc(legendX + 10, legendY + 10, 4, 0, 2 * Math.PI);
    ctx.fill();
    ctx.fillStyle = '#333';
    ctx.fillText('Customers', legendX + 20, legendY + 15);

    // Closed facility
    ctx.fillStyle = '#ef4444';
    ctx.fillRect(legendX + 10, legendY + 25, 8, 8);
    ctx.fillStyle = '#333';
    ctx.fillText('Closed Facility', legendX + 25, legendY + 33);

    // Open facility
    ctx.fillStyle = '#10b981';
    ctx.fillRect(legendX + 110, legendY + 25, 8, 8);
    ctx.fillStyle = '#333';
    ctx.fillText('Open Facility', legendX + 125, legendY + 33);
}

// ===============================
// UTILITIES
// ===============================

function showError(message) {
    errorMessage.textContent = message;
    errorContainer.style.display = 'block';
}

function hideError() {
    errorContainer.style.display = 'none';
}

function clearUI() {
    resultContainer.style.display = 'none';
    resultData.innerHTML = '';
    currentSolution = null;
}

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