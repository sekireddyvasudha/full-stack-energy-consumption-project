const form = document.getElementById("predictForm");
const inputDiv = document.getElementById("inputs");
const resultDiv = document.getElementById("result");
const chartCtx = document.getElementById("chart").getContext("2d");
let chart = null;
let inputData = [];

document.getElementById("loadBtn").addEventListener("click", async () => {
  const res = await fetch("http://127.0.0.1:5000/load-sample-data");
  const data = await res.json();
  inputData = data.input;
  renderInputs(inputData);
});

function renderInputs(data) {
  inputDiv.innerHTML = "";
  data.forEach((row, i) => {
    row.forEach((value, j) => {
      const input = document.createElement("input");
      input.type = "number";
      input.step = "any";
      input.value = value;
      input.required = true;
      input.name = `r${i}c${j}`;
      inputDiv.appendChild(input);
    });
    inputDiv.appendChild(document.createElement("br"));
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const rows = [];
  for (let i = 0; i < 5; i++) {
    const row = [];
    for (let j = 0; j < 8; j++) {
      const val = parseFloat(form[`r${i}c${j}`].value);
      if (isNaN(val)) return alert("All values must be numbers.");
      row.push(val);
    }
    rows.push(row);
  }

  const res = await fetch("http://127.0.0.1:5000/predict", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ input: rows }),
  });
  const data = await res.json();
  resultDiv.innerText = `Predicted Energy Consumption: ${data.prediction.toFixed(2)}`;

  renderChart(data.prediction);
});

function renderChart(value) {
  if (chart) chart.destroy();
  chart = new Chart(chartCtx, {
    type: "bar",
    data: {
      labels: ["Prediction"],
      datasets: [{
        label: "Energy Consumption",
        data: [value],
        backgroundColor: "rgba(54, 162, 235, 0.5)",
        borderColor: "rgba(54, 162, 235, 1)",
        borderWidth: 1
      }]
    },
    options: {
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}
