const express = require('express');
const cors = require('cors');

const app = express();

// Enable CORS for all URLs
app.use(cors());

// Import the predict function from another file
const {predict} = require('./predict');

// Define a route that calls the predict function
app.get('/predict', async (req, res) => {
    try {
        const inputParam = req.query.param; // Assuming the parameter is passed as a query parameter named 'param'

        // Call the predict function with the inputParam
        const result = await predict(inputParam);
        const stringValue = result.prediction[0].structValue.fields.candidates
            .listValue.values[0].structValue.fields.content.stringValue;
        const stringValues = [];
        console.log(result.prediction.map((prediction) => {
            return prediction.structValue.fields.candidates.listValue.values.map((value) => {
                return value.structValue.fields.content.stringValue;
            });
        }));

        result.prediction.forEach((prediction) => {
            (prediction.structValue.fields.candidates.listValue.values.forEach((value) => {
                stringValues.push(value.structValue.fields.content.stringValue);
            }));
        });

        res.json(stringValues);
    } catch (error) {
        console.error(error);
        res.status(500).json({error: 'An error occurred'});
    }
});

// Start the server
const port = 3000;
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});