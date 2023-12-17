const express = require('express');
const app = express();

app.use(express.static('public'));

app.post('/record', (req, res) => {
    // Perform speech recognition logic here
    // Send back the recognized text as response
    res.send('Recognized speech text');
});

const port = 3000;
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});