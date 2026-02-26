// Frontend JavaScript for the facility location optimization application

// Configuration
const GRID_SIZE = 100; // 100x100 unit grid
const CANVAS_SIZE = 500; // Canvas size in pixels
const SCALE = CANVAS_SIZE / GRID_SIZE; // Pixels per grid unit

// State
let currentInstance = null;
let randomSolution = null;
let optimalSolution = null;

// Get DOM elements
const generateForm = document.getElementById('generateForm');
const solveButton = document.getElementById('solveButton');
const solveOptimallyButton = document.getElementById('solveOptimallyButton');
const resultContainer = document.getElementById('resultContainer');
const resultData = document.getElementById('resultData');
const errorContainer = document.getElementById('errorContainer');
const errorMessage = document.getElementById('errorMessage');
const chartContainer = document.getElementById('chartContainer');
const chartCanvas = document.getElementById('chartCanvas');
const mapPanel = document.getElementById('mapPanel');
const gridCanvasInstance = document.getElementById('gridCanvasInstance');
const gridCanvasRandom = document.getElementById('gridCanvasRandom');
const gridCanvasOptimal = document.getElementById('gridCanvasOptimal');
const randomCanvasWrapper = document.getElementById('randomCanvasWrapper');
const optimalCanvasWrapper = document.getElementById('optimalCanvasWrapper');

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
            headers: { 'Content-Type': 'application/json' },
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

        currentInstance = await response.json();

        displayResults(currentInstance);
        drawGrid(gridCanvasInstance, currentInstance);

        mapPanel.style.display = 'flex';
        resultContainer.style.display = 'block';
        solveButton.style.display = 'inline-block';
        solveOptimallyButton.style.display = 'inline-block';

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

async function solveInstance(endpoint, button, buttonLabel, canvasWrapper, canvas, storeSolution) {
    if (!currentInstance) return;

    hideError();
    button.disabled = true;
    button.textContent = 'Solving...';

    try {
        const response = await fetch(endpoint, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(currentInstance),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`${response.status}: ${errorText}`);
        }

        const solution = await response.json();
        storeSolution(solution);

        canvasWrapper.style.display = 'flex';
        drawGrid(canvas, currentInstance, solution);
        drawChart();

    } catch (error) {
        showError(`Error solving instance: ${error.message}`);
    } finally {
        button.disabled = false;
        button.textContent = buttonLabel;
    }
}

solveButton.addEventListener('click', () =>
    solveInstance(
        '/api/solve-instance-randomly',
        solveButton,
        'Solve instance randomly',
        randomCanvasWrapper,
        gridCanvasRandom,
        (solution) => { randomSolution = solution; }
    )
);

solveOptimallyButton.addEventListener('click', () =>
    solveInstance(
        '/api/solve-instance-optimally',
        solveOptimallyButton,
        'Solve instance optimally',
        optimalCanvasWrapper,
        gridCanvasOptimal,
        (solution) => { optimalSolution = solution; }
    )
);

// ===============================
// DISPLAY RESULTS
// ===============================

function displayResults(instance) {
    const dataStr = JSON.stringify(instance, null, 2);
    resultData.innerHTML = `<pre>${escapeHtml(dataStr)}</pre>`;
}

// ===============================
// DRAW GRID
// ===============================

function drawGrid(canvas, instance, solution = null) {
    const ctx = canvas.getContext('2d');

    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, CANVAS_SIZE, CANVAS_SIZE);

    drawGridLines(ctx);

    if (solution) {
        drawAssignments(ctx, instance, solution);
    }

    drawCustomers(ctx, instance);
    drawFacilities(ctx, instance, solution);
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

        const isOpen = solution && solution.open_facilities.includes(index);
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

// ===============================
// DRAW CHART
// ===============================

function drawChart() {
    const hasSolutions = randomSolution || optimalSolution;
    if (!hasSolutions) return;

    const W = 500;
    const H = 350;
    const paddingTop = 30;
    const paddingBottom = 60;
    const paddingLeft = 70;
    const paddingRight = 30;
    const chartW = W - paddingLeft - paddingRight;
    const chartH = H - paddingTop - paddingBottom;

    chartCanvas.width = W;
    chartCanvas.height = H;
    chartContainer.style.display = 'block';

    const ctx = chartCanvas.getContext('2d');
    ctx.clearRect(0, 0, W, H);
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(0, 0, W, H);

    const maxCost = Math.max(
        randomSolution ? randomSolution.total_cost : 0,
        optimalSolution ? optimalSolution.total_cost : 0
    ) * 1.15;

    const COLOR_FACILITY = '#667eea';
    const COLOR_TRANSPORT = '#10b981';

    const slotW = chartW / 2;
    const barW = slotW * 0.5;
    const slots = [
        { label: 'Random', solution: randomSolution, x: paddingLeft + slotW * 0.5 - barW / 2 },
        { label: 'Optimal', solution: optimalSolution, x: paddingLeft + slotW * 1.5 - barW / 2 },
    ];

    // Y-axis gridlines and labels
    const nTicks = 5;
    ctx.textAlign = 'right';
    ctx.font = '11px sans-serif';
    ctx.fillStyle = '#666';
    for (let i = 0; i <= nTicks; i++) {
        const value = (maxCost / nTicks) * i;
        const y = paddingTop + chartH - (value / maxCost) * chartH;

        ctx.strokeStyle = '#e0e0e0';
        ctx.lineWidth = 0.5;
        ctx.beginPath();
        ctx.moveTo(paddingLeft, y);
        ctx.lineTo(paddingLeft + chartW, y);
        ctx.stroke();

        ctx.fillStyle = '#666';
        ctx.fillText(Math.round(value), paddingLeft - 8, y + 4);
    }

    // Y-axis label
    ctx.save();
    ctx.translate(14, paddingTop + chartH / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.textAlign = 'center';
    ctx.font = '12px sans-serif';
    ctx.fillStyle = '#333';
    ctx.fillText('Cost', 0, 0);
    ctx.restore();

    // Draw bars
    slots.forEach(({ label, solution, x }) => {
        if (!solution) {
            ctx.fillStyle = '#e0e0e0';
            ctx.fillRect(x, paddingTop, barW, chartH);
            ctx.fillStyle = '#999';
            ctx.textAlign = 'center';
            ctx.font = '11px sans-serif';
            ctx.fillText('—', x + barW / 2, paddingTop + chartH / 2);
        } else {
            const facilityH = (solution.total_opening_cost / maxCost) * chartH;
            const transportH = (solution.total_transportation_cost / maxCost) * chartH;
            const facilityY = paddingTop + chartH - facilityH;
            const transportY = facilityY - transportH;

            ctx.fillStyle = COLOR_FACILITY;
            ctx.fillRect(x, facilityY, barW, facilityH);

            ctx.fillStyle = COLOR_TRANSPORT;
            ctx.fillRect(x, transportY, barW, transportH);

            ctx.fillStyle = '#333';
            ctx.textAlign = 'center';
            ctx.font = 'bold 11px sans-serif';
            ctx.fillText(Math.round(solution.total_cost), x + barW / 2, transportY - 6);
        }

        ctx.fillStyle = '#333';
        ctx.textAlign = 'center';
        ctx.font = '12px sans-serif';
        ctx.fillText(label, x + barW / 2, paddingTop + chartH + 20);
    });

    // X-axis line
    ctx.strokeStyle = '#333';
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(paddingLeft, paddingTop + chartH);
    ctx.lineTo(paddingLeft + chartW, paddingTop + chartH);
    ctx.stroke();

    // Legend
    const legendX = paddingLeft;
    const legendY = paddingTop + chartH + 36;
    const items = [
        { color: COLOR_FACILITY, label: 'Facility Opening Cost' },
        { color: COLOR_TRANSPORT, label: 'Transportation Cost' },
    ];
    let lx = legendX;
    items.forEach(({ color, label }) => {
        ctx.fillStyle = color;
        ctx.fillRect(lx, legendY, 12, 12);
        ctx.fillStyle = '#333';
        ctx.textAlign = 'left';
        ctx.font = '11px sans-serif';
        ctx.fillText(label, lx + 16, legendY + 10);
        lx += 180;
    });
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
    mapPanel.style.display = 'none';
    randomCanvasWrapper.style.display = 'none';
    optimalCanvasWrapper.style.display = 'none';
    chartContainer.style.display = 'none';
    currentInstance = null;
    randomSolution = null;
    optimalSolution = null;
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