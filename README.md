# 🏙️ Smart Civic Complaint Intelligence System

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Scikit-learn"/>
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" alt="Git"/>
</p>

<p align="center">
  <b>Machine Learning | Civic Technology | Data Analysis</b>
</p>

---

## 📌 Project Overview

The **Smart Civic Complaint Intelligence System** is a machine learning-based project designed to analyse civic complaints and identify patterns related to complaint escalation and resolution.

The project explores how data analysis and machine learning can support a better understanding of civic complaint management.

## ❗ Problem Statement

Civic authorities receive complaints related to waste management, road damage, water supply and public infrastructure.

Managing these complaints efficiently can be challenging due to variations in complaint severity, workload and resolution time.

This project explores how machine learning can help analyse complaint data and identify complaints that may require additional attention.

## 🎯 Objectives

- Analyse civic complaint data.
- Identify patterns in complaint escalation.
- Study factors affecting complaint resolution time.
- Apply machine learning techniques to civic complaint data.
- Present analytical insights through a dashboard.

## ✨ Key Features

- Civic complaint data analysis.
- Complaint escalation prediction.
- Complaint resolution pattern analysis.
- Machine learning-based insights.
- Interactive dashboard for presenting analytical results.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Streamlit | Web dashboard |
| Pandas | Data analysis |
| Scikit-learn | Machine learning |
| Joblib | Model serialization |
| Altair | Data visualization |
| Git & GitHub | Version control |

## 📊 Dataset Information

- **Dataset:** Mumbai Nagar Seva – BMC Civic Complaint Resolution (2018–2024)
- **Source:** Kaggle
- **Domain:** Civic Complaint Management
- **Location:** Mumbai, India

The dataset contains civic complaint-related information used to explore complaint patterns, escalation and resolution.

> **Note:** The original dataset is not included in this repository because of its large file size. Download it from its original Kaggle source before running the project.

## 📁 Project Structure

```text
smart-civic-complaint-intelligence/
│
├── app.py
├── analytics.py
├── preprocess.py
├── train_model.py
├── train_escalation_model.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Nisha-hy/smart-civic-complaint-intelligence.git
```

### 2. Navigate to the project directory

```bash
cd smart-civic-complaint-intelligence
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## 📂 Dataset Setup

1. Download the required `bmc_train.csv` dataset from Kaggle.
2. Place the downloaded CSV file in the project root directory.
3. Ensure the filename is exactly `bmc_train.csv`.

## ▶️ Run the Project

### Train the satisfaction prediction model

```bash
python train_model.py
```

### Launch the Streamlit dashboard

```bash
streamlit run app.py
```

## 🔮 Future Enhancements

- Improve prediction performance through model evaluation and tuning.
- Add more interactive data visualizations.
- Explore additional factors influencing complaint resolution.
- Enhance dashboard usability.

## 👩‍💻 Author

**Nisha H Y**

Electronics and Communication Engineering

GitHub: [@Nisha-hy](https://github.com/Nisha-hy)

---

<p align="center">
  ⭐ If you find this project interesting, consider giving the repository a star!
</p>
