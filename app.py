import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(page_title="Starbucks Calorie Predictor", page_icon="☕", layout="centered")

# --- CLEAN PROFESSIONAL CSS ---
st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    div.stButton > button {
        width: 100% !important; border-radius: 10px !important;
        padding: 12px !important; font-weight: 700 !important; font-size: 16px !important;
    }
    .info-box {
        background: #F8FAFC; border: 1px solid #E2E8F0;
        padding: 14px 16px; border-radius: 12px; font-size: 14px;
    }
    .result-high {
        background: #FEF2F2; border: 1px solid #FECACA;
        padding: 18px; border-radius: 12px; text-align: center;
    }
    .result-low {
        background: #F0FDF4; border: 1px solid #BBF7D0;
        padding: 18px; border-radius: 12px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("☕ Starbucks Drink Calorie Predictor")
st.write("Predict whether your Starbucks drink is **High Calorie (>150 kcal)** or **Low / Medium Calorie (≤150 kcal)** based on its nutrition values.")
st.markdown("---")

@st.cache_resource
def load_model():
    return joblib.load('starbucks_decision_tree_model.joblib')

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.subheader("Enter Nutrition Details")

# 3 Columns for Clean Look
c1, c2, c3 = st.columns(3)
with c1:
    fat = st.number_input("Fat (g)", min_value=0.0, max_value=30.0, value=2.0, step=0.5)
with c2:
    carb = st.number_input("Carbohydrates (g)", min_value=0.0, max_value=100.0, value=25.0, step=1.0)
with c3:
    protein = st.number_input("Protein (g)", min_value=0.0, max_value=30.0, value=4.0, step=0.5)

st.markdown("<br>", unsafe_allow_html=True)

# Sliders bhi rakhe hain - neeche compact
st.write("Adjust with Sliders")
fat = st.slider("Fat (g)", min_value=0.0, max_value=30.0, value=float(fat), step=0.5)
carb = st.slider("Carbohydrates (g)", min_value=0.0, max_value=100.0, value=float(carb), step=1.0)
protein = st.slider("Protein (g)", min_value=0.0, max_value=30.0, value=float(protein), step=0.5)

# Estimated Calories Show
est_cal = fat*9 + carb*4 + protein*4
st.markdown(f'<div class="info-box">📊 <b>Estimated Calories from Macros:</b> ~ {est_cal:.0f} kcal &nbsp; | &nbsp; Fat: {fat}g &nbsp;•&nbsp; Carbs: {carb}g &nbsp;•&nbsp; Protein: {protein}g</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Predict Calorie Category", type="primary"):
    input_data = pd.DataFrame([[fat, carb, protein]], columns=['Fat (g)', 'Carb. (g)', 'Protein'])
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]
    
    st.markdown("---")
    if prediction == 1:
        conf = probabilities[1]*100
        st.markdown(f'<div class="result-high"><h3 style="color:#DC2626; margin:0;">🚨 High Calorie</h3><p style="margin:8px 0 0 0;"><b>&gt;150 Calories</b> • Confidence: <b>{conf:.1f}%</b></p><p style="font-size:13px; color:#6B7280; margin:6px 0 0 0;">This drink is high in calories. Consider a smaller size or low-fat option.</p></div>', unsafe_allow_html=True)
    else:
        conf = probabilities[0]*100
        st.markdown(f'<div class="result-low"><h3 style="color:#16A34A; margin:0;">✅ Low / Medium Calorie</h3><p style="margin:8px 0 0 0;"><b>≤150 Calories</b> • Confidence: <b>{conf:.1f}%</b></p><p style="font-size:13px; color:#6B7280; margin:6px 0 0 0;">Good choice! This drink is within a moderate calorie range.</p></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.write(f"Model Confidence: {conf:.1f}%")
    st.progress(int(conf))

    if st.button("🔄  Try Another Drink"):
        st.rerun()

st.markdown("---")
st.markdown('<p style="text-align:center; color:grey; font-size:12px;">Starbucks Calorie Predictor • Decision Tree Model • Final Year Project</p>', unsafe_allow_html=True)
