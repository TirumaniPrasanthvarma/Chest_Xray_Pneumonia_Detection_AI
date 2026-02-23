# 🫁 Chest X-Ray Pneumonia Detection AI Web Application

An end-to-end AI-powered web application that detects Pneumonia from Chest X-ray images using Deep Learning.

This project integrates Artificial Intelligence, Web Development, and Database Systems into one complete real-world application. It allows users to securely register, upload chest X-ray images, receive AI-based predictions, and store results in a structured MySQL database.

The purpose of this project is to demonstrate how a trained deep learning model can be deployed as a fully functional web system with authentication, database logging, and a modern user interface.

---

## 🚀 Project Overview

This system consists of three major components:

1. Deep Learning Model (ResNet18 - Transfer Learning)
2. Web Application Interface (Streamlit)
3. MySQL Database Integration

Application Flow:

1️⃣ User visits Welcome Page  
2️⃣ User registers or logs in  
3️⃣ User accesses Dashboard  
4️⃣ User uploads a Chest X-ray image  
5️⃣ AI model predicts Pneumonia or Normal  
6️⃣ Confidence score is displayed  
7️⃣ Result is stored in MySQL database  

---

## 🧠 AI Model Details

- Base Model: ResNet18 (Pretrained on ImageNet)
- Task: Binary Classification (Pneumonia vs Normal)
- Loss Function: BCEWithLogitsLoss
- Optimizer: Adam
- Image Input Size: 224 × 224
- Output Layer: Single neuron (Binary output)
- Activation: Sigmoid (during inference)

Transfer learning was used by replacing the final fully connected layer of ResNet18 to adapt it for binary classification.

---

## 📂 Dataset Structure

The dataset is organized as:

```
train/
    NORMAL/
    PNEUMONIA/

test/
    NORMAL/
    PNEUMONIA/
```

- Images resized to 224x224
- Two categories:
  - NORMAL
  - PNEUMONIA
- Binary classification problem

⚠ Full dataset is not uploaded due to GitHub size limitations. Only sample images (if included) are provided for structure reference.

---

## 🔐 Authentication System

The application includes:

- User Registration
- Secure Login System
- Session Management
- Logout Functionality

Users must log in to access the AI prediction dashboard.

---

## 🗄 Database Architecture

The application uses MySQL to store user and prediction data.

### Users Table

| Column   | Type |
|----------|------|
| id       | INT (Primary Key) |
| username | VARCHAR |
| password | VARCHAR |

### Predictions Table

| Column      | Type |
|------------|------|
| id         | INT |
| username   | VARCHAR |
| prediction | VARCHAR |
| confidence | FLOAT |
| timestamp  | DATETIME |

Each prediction is stored along with:
- Username
- Predicted class
- Confidence score
- Timestamp

---

## 🎨 UI & Design Features

- Animated Welcome Screen
- Modern White Gradient Design
- Clean Login & Register Page
- Dashboard Interface
- Real-time Prediction Display
- Confidence Level Indicator
- Smooth Page Transitions

---

## 🛠 Technologies Used

- Python
- PyTorch
- Torchvision
- Streamlit
- MySQL
- PIL (Python Imaging Library)

---

## 🖥 Installation Guide

### 1️⃣ Clone Repository

```
git clone https://github.com/yourusername/Chest-Xray-AI-App.git
```

### 2️⃣ Navigate to Project

```
cd Chest-Xray-AI-App
```

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

### 4️⃣ Setup MySQL Database

Create database:

```
CREATE DATABASE xray_app;
```

Create required tables:

```
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    prediction VARCHAR(50),
    confidence FLOAT,
    timestamp DATETIME
);
```

### 5️⃣ Run Application

```
streamlit run app.py
```

---

## 📈 Future Improvements

- Password hashing for enhanced security
- Admin analytics dashboard
- Prediction history page for users
- Model performance visualization
- Online cloud deployment

---

## ⚠ Disclaimer

This project is developed for educational and demonstration purposes only.  
It is not intended for real medical diagnosis or clinical use.

---

## 👨‍💻 Author

Prasanth Varma  
AIML Internship Project