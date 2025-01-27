const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const { spawn } = require('child_process');
const app = express();

let temperatureData = {};

app.use(express.json());
app.use(express.static(path.join(__dirname))); // Serve static files from root directory

// Add default route to serve home.html
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'home.html'));
});

// Save floor plan
app.post('/api/save', async (req, res) => {
    try {
        const layout = Array.isArray(req.body) ? req.body : [];
        const fileName = `floorplan_${new Date().toISOString().slice(0,10)}.json`;
        const filePath = path.join(__dirname, 'layouts', fileName);
        
        // Ensure layouts directory exists
        await fs.mkdir(path.join(__dirname, 'layouts'), { recursive: true });
        
        // Save the file
        await fs.writeFile(filePath, JSON.stringify(layout, null, 2));
        res.json({ success: true, fileName });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// List available layouts
app.get('/api/layouts', async (req, res) => {
    try {
        const layoutsDir = path.join(__dirname, 'layouts');
        await fs.mkdir(layoutsDir, { recursive: true });
        const files = await fs.readdir(layoutsDir);
        // Only return files that start with 'floorplan_'
        const floorplanFiles = files.filter(file => file.startsWith('floorplan_'));
        res.json(floorplanFiles);
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Load specific layout
app.get('/api/load/:filename', async (req, res) => {
    try {
        const filePath = path.join(__dirname, 'layouts', req.params.filename);
        const data = await fs.readFile(filePath, 'utf8');
        const layout = JSON.parse(data);
        res.json(Array.isArray(layout) ? layout : []);
    } catch (error) {
        console.error('Error loading layout:', error);
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/temperatures', (req, res) => {
    res.json(temperatureData);
});

app.post('/api/sensor-mapping', async (req, res) => {
    try {
        const mappingPath = path.join(__dirname, 'layouts', 'sensor_mapping.json');
        await fs.writeFile(mappingPath, JSON.stringify(req.body, null, 2));
        res.json({ success: true });
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

app.get('/api/sensor-mapping', async (req, res) => {
    try {
        const mappingPath = path.join(__dirname, 'layouts', 'sensor_mapping.json');
        const data = await fs.readFile(mappingPath, 'utf8');
        res.json(JSON.parse(data));
    } catch (error) {
        res.status(500).json({ error: error.message });
    }
});

// Start Python script for temperature monitoring
const pythonProcess = spawn('python', ['templogger.py']);

pythonProcess.stdout.on('data', (data) => {
    try {
        const tempData = JSON.parse(data);
        temperatureData = tempData;
    } catch (e) {
        // Silently ignore parsing errors
    }
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
