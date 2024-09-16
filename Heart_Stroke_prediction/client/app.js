document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('predictionForm');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent the form from reloading

        // Clear previous results
        resultDiv.innerHTML = '';

        // Gather form data
        const formData = new FormData(form);
        const data = {
            gender: formData.get('gender'),
            smoking_status: formData.get('smoking_status'),
            age: formData.get('age'),
            hypertension: formData.get('hypertension'),
            heart_disease: formData.get('heart_disease'),
            avg_glucose_level: formData.get('avg_glucose_level'),
            bmi: formData.get('bmi')
        };

        try {
            // Send the data to the Flask server using POST
            const response = await fetch('http://localhost:5000/heart_stroke_prediction', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // Parse the response JSON
            const result = await response.json();

            // Check if there's an error in the result
            if (result.error) {
                resultDiv.innerHTML = `<h2 style="color: red;">Error: ${result.error}</h2>`;
            } else {
                // Display the prediction result
                if (result.heart_stroke === 1) {
                    resultDiv.innerHTML = `<h2 style="color: red;">Heart Stroke Detected</h2>`;
                } else {
                    resultDiv.innerHTML = `<h2 style="color: green;">No Heart Stroke</h2>`;
                }
            }
        } catch (error) {
            console.error('Error:', error);
            resultDiv.innerHTML = `<h2 style="color: red;">Error: ${error.message}</h2>`;
        }
    });
});
