const { spawn } = require('child_process');
const path = require('path');

// Start the Python script with correct path resolution
const pythonScript = path.join(__dirname, 'templogger.py');
const pythonProcess = spawn('python', [pythonScript], {
    stdio: ['ignore', 'pipe', 'inherit']
});

// Handle Python process output
pythonProcess.stdout.on('data', (data) => {
    try {
        const temperatureData = JSON.parse(data);
        // Log temperature data if needed
        console.log('Temperature data:', temperatureData);
    } catch (error) {
        console.error('Error parsing temperature data:', error.message);
    }
});

// Start the Node.js server
require('./server.js');

// Wait a short time for the server to start, then open the browser
setTimeout(async () => {
    const open = await import('open');
    await open.default('http://localhost:3000/viewer.html');
}, 1000);

// Handle cleanup when the Node.js process exits
process.on('SIGINT', () => {
    pythonProcess.kill();
    process.exit();
});

process.on('SIGTERM', () => {
    pythonProcess.kill();
    process.exit();
});
