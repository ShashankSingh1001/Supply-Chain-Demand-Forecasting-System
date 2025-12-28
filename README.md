# 🚀 Supply Chain Optimization - MLOps Project

> **A production-grade, end-to-end machine learning system for demand forecasting and inventory optimization**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MLflow](https://img.shields.io/badge/MLflow-Tracking-blue)](https://mlflow.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-green)](https://www.docker.com/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [MLOps Pipeline](#mlops-pipeline)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project implements a **fully automated, data-driven supply chain pipeline** that continuously learns from sales data to improve forecast accuracy and support real-time decision-making for inventory, procurement, and logistics.

### Core Objectives

1. **Demand Forecasting**: Predict daily item-level demand across stores using time-series and ML models
2. **Inventory Optimization**: Determine optimal stock levels to minimize stockouts and overstock
3. **MLOps Automation**: Implement reproducible, scalable pipelines for data ingestion, model training, and deployment

### Dataset

This project uses the **Corporación Favorita** grocery sales dataset from Kaggle, which includes:
- Historical sales data
- Store information
- Item details
- Holiday and event calendars
- Oil prices
- Transaction volumes

---

## ✨ Features

- 🔮 **Advanced Forecasting**: Time-series models (ARIMA, Prophet) and gradient boosting (XGBoost, LightGBM)
- 📊 **Interactive Dashboard**: Real-time visualization of forecasts and inventory recommendations
- 🔄 **Automated Pipelines**: End-to-end MLOps with CI/CD integration
- 📈 **Experiment Tracking**: MLflow for versioning and model management
- 🐳 **Containerized**: Docker support for reproducible deployments
- 🧪 **Comprehensive Testing**: Unit and integration tests with pytest
- 📉 **Monitoring**: Data drift detection and model performance tracking
- 🎨 **Custom Logging**: Centralized, structured logging system

---

## 🛠️ Tech Stack

### Machine Learning & Data Science
- **Python 3.8+** | **Pandas** | **NumPy** | **Scikit-learn**
- **XGBoost** | **LightGBM** | **Prophet** | **Statsmodels**
- **Matplotlib** | **Seaborn** | **Plotly**

### MLOps & Automation
- **MLflow** - Experiment tracking and model registry
- **Docker** - Containerization
- **GitHub Actions** - CI/CD pipelines
- **DVC** *(optional)* - Data version control

### Software Engineering
- **Custom Logging System** - Centralized logging
- **Custom Exception Handling** - Traceable errors
- **Pytest** - Testing framework
- **Pre-commit Hooks** - Code quality

### Visualization & Dashboard
- **Streamlit** - Interactive web dashboard

---

## 📁 Project Structure

```
supply-chain-optimization/
├── config/                    # Configuration files
├── data/                      # Data storage (raw, processed, predictions)
├── notebooks/                 # Jupyter notebooks for EDA
├── supply_chain/              # Main source code package
│   ├── components/            # Pipeline components
│   ├── pipelines/             # Training and prediction workflows
│   ├── models/                # Model definitions
│   └── inventory/             # Inventory optimization logic
├── mlops/                     # MLOps infrastructure
│   ├── experiment_tracking/   # MLflow setup
│   ├── monitoring/            # Data drift & performance tracking
│   └── deployment/            # Deployment scripts
├── tests/                     # Unit and integration tests
├── dashboard/                 # Streamlit dashboard
├── scripts/                   # Standalone execution scripts
└── .github/workflows/         # CI/CD pipelines
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip or conda
- Git
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/supply-chain-optimization.git
cd supply-chain-optimization
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Install package in editable mode**
```bash
pip install -e .
```

5. **Download dataset**
```bash
python scripts/download_data.py
```

6. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configurations
```

---

## 💻 Usage

### Training Pipeline

```bash
python scripts/run_training.py
```

### Prediction Pipeline

```bash
python scripts/run_prediction.py
```

### Launch Dashboard

```bash
streamlit run dashboard/app.py
```

### Run Tests

```bash
pytest tests/
```

### MLflow UI

```bash
mlflow ui
```

---

## 🔄 MLOps Pipeline

### 1. Data Ingestion
- Load raw data from multiple sources
- Validate data quality and schema

### 2. Data Transformation
- Feature engineering
- Time-series feature extraction
- Data preprocessing

### 3. Model Training
- Train multiple models (baseline, time-series, ML)
- Hyperparameter tuning
- Cross-validation

### 4. Model Evaluation
- Calculate performance metrics (RMSE, MAE, MAPE)
- Compare models
- Select best model

### 5. Model Registration
- Version models with MLflow
- Tag and annotate models

### 6. Deployment
- Deploy best model
- Serve predictions via API

### 7. Monitoring
- Track model performance
- Detect data drift
- Trigger retraining when needed

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - your.email@example.com

Project Link: [https://github.com/yourusername/supply-chain-optimization](https://github.com/yourusername/supply-chain-optimization)

---

## 🙏 Acknowledgments

- [Corporación Favorita Dataset](https://www.kaggle.com/c/favorita-grocery-sales-forecasting) on Kaggle
- MLflow community
- Open-source contributors

---

**⭐ Star this repo if you find it useful!**