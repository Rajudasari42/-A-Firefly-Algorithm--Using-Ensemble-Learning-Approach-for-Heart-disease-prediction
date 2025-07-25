let chart; // global chart variable

// Function to make the prediction
async function predict() {
    const features = [
        parseFloat(document.getElementById("age").value),
        parseFloat(document.getElementById("sex").value),
        parseFloat(document.getElementById("cp").value),
        parseFloat(document.getElementById("trestbps").value),
        parseFloat(document.getElementById("chol").value),
        parseFloat(document.getElementById("fbs").value),
        parseFloat(document.getElementById("restecg").value),
        parseFloat(document.getElementById("thalach").value),
        parseFloat(document.getElementById("exang").value),
        parseFloat(document.getElementById("oldpeak").value),
        parseFloat(document.getElementById("slope").value),
        parseFloat(document.getElementById("ca").value),
        parseFloat(document.getElementById("thal").value)
    ];

    if (features.some(isNaN)) {
        alert("Please fill in all fields with valid numbers.");
        return;
    }

    const progressBar = document.getElementById("progress-bar");
    progressBar.style.display = "block";

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ features: features })
        });

        const data = await response.json();

        // Display prediction result
        const resultElement = document.getElementById("result");
        if (data.prediction) {
            resultElement.textContent = `Prediction: ${data.prediction}`;
            resultElement.className = data.prediction === "High Risk" ? "high-risk show" : "low-risk show";
        } else {
            resultElement.textContent = `Error: ${data.error}`;
            resultElement.className = "";
        }

        // Show the chart
        showChart(features);

    } catch (error) {
        alert("Error connecting to the server: " + error);
    } finally {
        setTimeout(() => {
            progressBar.style.display = "none";
        }, 1000);
    }
}

// Function to reset the form
function resetForm() {
    document.getElementById("predictionForm").reset();
    document.getElementById("result").textContent = "";
    document.getElementById("result").className = "";

    // Destroy chart if exists
    if (chart) {
        chart.destroy();
    }
}

// Function to show chart
function showChart(features) {
    const ctx = document.getElementById("resultChart").getContext("2d");
    const labels = [
        "Age", "Sex", "CP", "BP", "Chol", "FBS",
        "ECG", "HR", "ExAng", "Oldpeak", "Slope", "CA", "Thal"
    ];

    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Patient Input Values',
                data: features,
                backgroundColor: '#007bff'
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false },
                title: {
                    display: true,
                    text: 'Prediction Input Features'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
