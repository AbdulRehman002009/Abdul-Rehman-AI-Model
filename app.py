import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Starbucks Calorie Predictor", page_icon="☕", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .block-container {padding-top: 2rem !important; padding-bottom: 1rem !important; max-width: 700px !important;}
    /* Starbucks Green Button */
    div.stButton > button {
        width: 100% !important; border-radius: 12px !important;
        padding: 14px !important; font-weight: 700 !important; font-size: 16px !important;
        background: #00704A !important; color: white !important; border: none !important;
    }
    div.stButton > button:hover { background: #005A3C !important; }
    /* Slider Green */
    div[data-testid="stSlider"] > div > div > div > div { background: #00704A !important; }
    .card {
        background: #FFFFFF; border: 1px solid #E5E7EB;
        border-radius: 16px; padding: 22px; box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
    .est-box {
        background: #F0F7F3; border: 1px solid #C8E6D5;
        padding: 14px; border-radius: 12px; text-align: center;
        font-size: 15px; color: #1E3A2F;
    }
    .result-high {
        background: #FEF2F2; border: 1px solid #FECACA;
        padding: 20px; border-radius: 14px; text-align: center;
    }
    .result-low {
        background: #F0FDF4; border: 1px solid #BBF7D0;
        padding: 20px; border-radius: 14px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown('<p style="font-size:42px; margin:0;">☕</p>', unsafe_allow_html=True)
st.title("Starbucks Calorie Predictor")
st.write("Check if your favourite Starbucks drink is **High Calorie** or **Low / Medium Calorie** — just enter its nutrition values.")
st.markdown("---")

@st.cache_resource
def load_model():
    return joblib.load('starbucks_decision_tree_model.joblib')

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- INPUT CARD - SIRF EK BAAR INPUT ---
with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🥤 Enter Nutrition Details")
    st.write("Move the sliders to match your drink's nutrition label.")

    fat = st.slider("Fat (g)", 0.0, 30.0, 2.0, 0.5)
    carb = st.slider("Carbohydrates (g)", 0.0, 100.0, 25.0, 1.0)
    protein = st.slider("Protein (g)", 0.0, 30.0, 4.0, 0.5)

    est_cal = fat*9 + carb*4 + protein*4
    st.markdown(f'<div class="est-box">📊 <b>Estimated Calories:</b> ~ <b>{est_cal:.0f} kcal</b> &nbsp;|&nbsp; Fat {fat}g • Carbs {carb}g • Protein {protein}g</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Predict Calorie Category"):
    input_data = pd.DataFrame([[fat, carb, protein]], columns=['Fat (g)', 'Carb. (g)', 'Protein'])
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    if prediction == 1:
        conf = probabilities[1]*100
        st.markdown(f'<div class="result-high"><h3 style="color:#DC2626; margin:0;">🚨 High Calorie Drink</h3><p style="margin:10px 0 0 0; font-size:16px;"><b>> 150 Calories</b> • Confidence: <b>{conf:.1f}%</b></p><p style="font-size:13px; color:#6B7280; margin:8px 0 0 0;">Tip: Try a smaller size, skim milk or less syrup.</p></div>', unsafe_allow_html=True)
    else:
        conf = probabilities[0]*100
        st.markdown(f'<div class="result-low"><h3 style="color:#16A34A; margin:0;">✅ Low / Medium Calorie Drink</h3><p style="margin:10px 0 0 0; font-size:16px;"><b>≤ 150 Calories</b> • Confidence: <b>{conf:.1f}%</b></p><p style="font-size:13px; color:#6B7280; margin:8px 0 0 0;">Great choice! This drink is in a moderate calorie range.</p></div>', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.progress(int(conf))
    st.caption(f"Model Confidence: {conf:.1f}%")

st.markdown("---")
st.markdown('<p style="text-align:center; color:#9CA3AF; font-size:12px;">Starbucks Calorie Predictor • Decision Tree Model • Final Year Project</p>', unsafe_allow_html=True)
