# Smart Civic Complaint Intelligence System
## Project Overview

The Smart Civic Complaint Intelligence System is a machine learning-based project designed to analyse civic complaints and identify patterns related to complaint escalation and resolution.

The project aims to support better understanding of civic complaint management through data analysis and machine learning.
## Problem Statement

Civic authorities receive complaints related to issues such as waste management, road damage, water supply and public infrastructure.

Managing these complaints efficiently can be challenging due to variations in complaint severity, workload and resolution time.

This project explores how machine learning can help analyse complaint data and identify complaints that may require additional attention.
## Objectives

- Analyse civic complaint data.
- Identify patterns in complaint escalation.
- Study factors affecting complaint resolution time.
- Apply machine learning techniques to civic complaint data.
- Present useful insights through a dashboard.
## Key Features

- Civic complaint data analysis.
- Complaint escalation prediction.
- Complaint resolution pattern analysis.
- Machine learning-based insights.
- Dashboard for presenting analytical results.
## Technologies Used

- **Programming Language:** Python
- **Web Framework:** Streamlit
- **Data Analysis:** Pandas
- **Machine Learning:** Scikit-learn
- **Model Serialization:** Joblib
- **Data Visualization:** Altair
- **Version Control:** Git and GitHub
- **Development Environment:** Visual Studio Code
## Dataset Information

- **Dataset:** Mumbai Nagar Seva – BMC Civic Complaint Resolution (2018–2024)
- **Source:** Kaggle
- **Domain:** Civic Complaint Management
- **Location:** Mumbai, India

The dataset contains civic complaint-related information that can be used to analyse complaint patterns, escalation and resolution.

Note: The original dataset is not included in this GitHub repository because of its large file size. Users must obtain the dataset from its original Kaggle source.
## Project Structure

civiccomplaintML/
│
├── app.py
├── analytics.py
├── preprocess.py
├── train_model.py
├── train_escalation_model.py
├── .gitignore
└── README.md
## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Nisha-hy/smart-civic-complaint-intelligence.git
cd smart-civic-complaint-intelligence
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Dataset Setup

This project uses the Mumbai Nagar Seva – BMC Civic Complaint Resolution (2018–2024) dataset from Kaggle.

1. Obtain the dataset from its original Kaggle source.
2. Download the training dataset.
3. Place the file named `bmc_train.csv` in the root project directory.

**Important:** The dataset is not included in this GitHub repository.

## How to Run the Project

### Step 1: Train the Machine Learning Model

```bash
python train_model.py
```

This script trains the citizen satisfaction classification model, evaluates its performance and saves the trained model as `civic_satisfaction_model.joblib`.

### Step 2: Launch the Dashboard

```bash
streamlit run app.py
```

The Streamlit dashboard will open in your web browser.
