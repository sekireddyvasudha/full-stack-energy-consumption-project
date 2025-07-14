# 🔋 Energy Consumption Prediction Web Application

This project is a web-based application for predicting energy consumption (or any time-series data) using machine learning models. Users can upload their dataset, specify the number of future time points they want to predict, and visualize the actual vs. predicted values on an interactive graph.

## 🚀 Features

- User Registration and Login system 🔐
- Upload CSV dataset
- Specify the number of future predictions
- Visualize Actual vs. Predicted values 📈
- Easy-to-use interface
- Logout functionality for session management

## 🧩 Tech Stack

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python (Flask or FastAPI — based on your setup)
- **Machine Learning:** 
  - Pandas
  - NumPy
  - Scikit-learn (or TensorFlow / Keras if using deep learning models)
  - Matplotlib or Plotly for visualization
- **Authentication:** Basic session-based login system
- **Deployment:** Localhost (can be deployed to Heroku, Render, or AWS)

## 📂 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/energy-prediction-app.git
   cd energy-prediction-app

Set up the virtual environment

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies

    pip install -r requirements.txt

Run the application

    python app.py

Open in browser Navigate to http://localhost:5000

📝 How to Use
Register for an account and log in.

Upload your dataset (CSV format, e.g., ENB2012_data.csv).

Enter the number of future time steps you want to predict.

Click Upload & Predict.

View the interactive graph showing predicted vs. actual values.

📊 Sample Dataset
You can use the provided ENB2012_data.csv or any time-series data that includes features relevant to energy consumption or forecasting.

🎯 Purpose
The goal of this application is to simplify machine learning predictions for non-technical users by providing an intuitive web interface. It makes it easy to forecast future trends and visualize results without coding knowledge.

💡 Future Enhancements
Add export option for predicted results (CSV/PDF)

Deploy to cloud platforms (Heroku, AWS, etc.)

Add email notification after predictions

Improve graph interactivity (zoom, pan, export)

Add more ML models (ARIMA, LSTM, etc.)

Add dark/light theme toggle

🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

🛡️ License
This project is licensed under the MIT License.

🙌 Acknowledgements
Scikit-learn Documentation

Flask / FastAPI Documentation

Dataset source: UCI Machine Learning Repository


