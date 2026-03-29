📈 YieldIQ — Investment Comparison System

An end-to-end data analytics and machine learning web application for comparing Indian investment instruments — LIC · Fixed Deposit · Gold · Mutual Funds
📌 Table of Contents

Overview
Live Demo
Key Features
Tech Stack
Project Structure
Dataset
ML Model
Installation
Author


🧠 Overview
YieldIQ is a full-stack data science web application built to help users make informed investment decisions by analysing and predicting returns across four major Indian investment instruments.
The platform combines exploratory data analysis, machine learning regression, and inferential statistics into a clean, interactive dashboard deployed on the cloud.
🎯 Problem Statement
Indian retail investors often lack accessible tools to compare investment options objectively. YieldIQ addresses this by providing data-driven insights, predictive modelling, and statistical validation — all in one place.

🌐 Live Demo
🔗 https://yieldi.streamlit.app

🚀 Key Features
🎯 Investment Prediction Engine

Predicts final investment value using a trained Random Forest Regressor
Inputs: Investment type, duration (1–25 years), principal amount (₹1K–₹1Cr)
Outputs: Final value, profit, ROI % with an animated projected growth chart

📊 Analytics Dashboard

Line chart — year-wise final value comparison across all asset classes
Bar chart — average ROI % per investment type
Donut chart — portfolio distribution by total investment
Box plot — profit distribution with outlier detection
Heatmap — year vs investment type ROI % matrix

🔬 Statistical Analysis

One-way ANOVA — tests if mean returns differ significantly across all 4 types
Independent T-Test — direct comparison of Mutual Funds vs Fixed Deposits
Violin plots — visual distribution comparison with significance verdict


🛠️ Tech Stack
LayerTechnologyFrontend / UIStreamlit 1.55, Custom CSSData ProcessingPandas 2.3, NumPy 2.4Machine Learningscikit-learn 1.8 (Random Forest Regressor)Statistical AnalysisSciPy 1.17 (ANOVA, T-Test)Data VisualisationPlotly 5.24.1 (interactive charts)DeploymentStreamlit Community CloudVersion ControlGit + GitHubRuntimePython 3.14

📁 Project Structure
yieldiq-investment-comparison-system/
│
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── combined_dataset.csv    # Historical investment dataset
├── retrain.py              # Script to retrain ML model
│
└── src/
    ├── predictor.py        # Prediction module
    ├── model.pkl           # Trained Random Forest model
    └── encoder.pkl         # Label encoder for investment types

📊 Dataset
ColumnTypeDescriptionInvestment_TypeCategoricalLIC / FD / Gold / Mutual FundYearIntegerInvestment duration (1–25 years)Total_InvestmentFloatPrincipal amount in INRFinal_ValueFloatMaturity value in INRProfitFloatFinal_Value − Total_InvestmentROI_%Float(Profit / Total_Investment) × 100

🤖 ML Model
ParameterDetailAlgorithmRandom Forest RegressorFeaturesYear, Total_Investment, Investment_Type (encoded)TargetFinal_ValueEstimators100 treesSerialisationPython pickle (.pkl)
To retrain the model:
bashpython retrain.py

⚙️ Installation
bash# Clone the repository
git clone https://github.com/Suraj03-ms/yieldiq-investment-comparison-system.git

# Navigate to project directory
cd yieldiq-investment-comparison-system

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
The app will open at http://localhost:8501

👨‍💻 Author
Suraj — Data Analytics Student

GitHub: https://github.com/Suraj03-ms
Live App: https://yieldi.streamlit.app


📄 License
This project is licensed under the MIT License.
