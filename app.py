# ==========================================================
# 1. IMPORTS
# ==========================================================

import os
import streamlit as st
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
import mysql.connector
from datetime import datetime

# ==========================================================
# 2. PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Chest X-Ray AI",
    page_icon="🫁",
    layout="centered"
)

# ==========================================================
# 3. PREMIUM WHITE UI CSS
# ==========================================================

st.markdown("""
<style>

/* White gradient background */
body {
    background: linear-gradient(135deg, #fdfbfb, #ebedee);
}

/* Animation */
@keyframes fadeSlide {
    from { opacity:0; transform:translateY(40px); }
    to { opacity:1; transform:translateY(0); }
}

/* Center card */
.center-card {
    background: white;
    padding: 50px;
    border-radius: 25px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    width: 420px;
    margin: auto;
    margin-top: 120px;
    animation: fadeSlide 0.8s ease-in-out;
}

/* Titles */
.hero-title {
    font-size: 50px;
    font-weight: bold;
    text-align: center;
    margin-top: 180px;
    color: #333;
    animation: fadeSlide 1s ease-in-out;
}

.hero-sub {
    text-align:center;
    font-size:20px;
    color:#666;
    margin-bottom:40px;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(45deg, #ff4e50, #f9d423);
    color: white;
    font-weight: bold;
    border-radius: 30px;
    height: 45px;
    width: 100%;
    border: none;
    font-size: 16px;
    transition: 0.3s;
}

div.stButton > button:hover {
    transform: scale(1.05);
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# 4. DATABASE
# ==========================================================

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT"))
    )

def register_user(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username,password) VALUES (%s,%s)",
            (username, password)
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()

def login_user(username, password):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# ==========================================================
# 5. SESSION STATE
# ==========================================================

if "page" not in st.session_state:
    st.session_state.page = "welcome"

if "username" not in st.session_state:
    st.session_state.username = ""

# ==========================================================
# 6. WELCOME PAGE
# ==========================================================

if st.session_state.page == "welcome":

    st.markdown('<div class="hero-title">🫁 Chest X-Ray AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">AI Powered Pneumonia Detection System</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 Start"):
            st.session_state.page = "auth"
            st.rerun()

# ==========================================================
# 7. LOGIN / REGISTER PAGE
# ==========================================================

elif st.session_state.page == "auth":

    st.markdown("<h2 style='text-align:center;'>🔐 Login or Register</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    # LOGIN
    with tab1:
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            user = login_user(username, password)
            if user:
                st.session_state.username = username
                st.session_state.page = "main"
                st.rerun()
            else:
                st.error("Invalid credentials")

    # REGISTER
    with tab2:
        new_user = st.text_input("Choose Username", key="reg_user")
        new_pass = st.text_input("Choose Password", type="password", key="reg_pass")

        if st.button("Create Account"):
            if register_user(new_user, new_pass):
                st.success("Account created successfully!")
            else:
                st.error("Username already exists")

    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# 8. MAIN DASHBOARD
# ==========================================================

elif st.session_state.page == "main":

    st.title("🫁 Pneumonia Detection Dashboard")
    st.success(f"Welcome, {st.session_state.username}")

    if st.button("Logout"):
        st.session_state.page = "welcome"
        st.rerun()

    MODEL_PATH = "model.pth"

    def build_resnet():
        model = models.resnet18(pretrained=False)
        in_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Linear(in_features,512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512,1)
        )
        return model

    model = build_resnet()
    model.load_state_dict(torch.load(MODEL_PATH, map_location="cpu"))
    model.eval()

    transform = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.485,0.456,0.406],
            [0.229,0.224,0.225]
        )
    ])

    uploaded_file = st.file_uploader("Upload Chest X-Ray Image", type=["jpg","jpeg","png"])

    if uploaded_file:

        image = Image.open(uploaded_file).convert("RGB")
        st.image(image, width=500)

        input_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            output = model(input_tensor)
            probability = torch.sigmoid(output).item()

        confidence = probability * 100

        if probability > 0.5:
            prediction = "Pneumonia"
            st.error(f"Prediction: {prediction}")
        else:
            prediction = "Normal"
            st.success(f"Prediction: {prediction}")

        st.info(f"Confidence: {confidence:.2f}%")

        # Save to DB
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO predictions (username,prediction,confidence,timestamp) VALUES (%s,%s,%s,%s)",
            (st.session_state.username, prediction, confidence, datetime.now())
        )
        conn.commit()
        cursor.close()
        conn.close()

# ==========================================================
# 10. FOOTER
# ==========================================================

st.markdown("---")
st.caption("ML Class Team Project")
