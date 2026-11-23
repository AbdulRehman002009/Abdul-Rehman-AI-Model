import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Starbucks Calorie Predictor", page_icon="☕", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .block-container { padding-top: 2rem !important; }
    div.stButton > button {
        width: 100% !important; border-radius: 12px !important; padding: 14px !important;
        font-weight: 700 !important; font-size: 16px !important;
        background: #111827 !important; color: white !important; border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER - Native, kabhi katega nahi ---
st.markdown('<span style="background:#E8F5EF; color:#00704A; font-size:12px; font-weight:700; padding:6px 12px; border-radius:100px;">● MACHINE LEARNING • DECISION TREE</span>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
st.title("Starbucks Drink Calorie Predictor")
st.caption("Enter your drink's nutrition values and instantly check if it's a High Calorie or Low / Medium Calorie choice.")

@st.cache_resource
def load_model():
    return joblib.load('starbucks_decision_tree_model.joblib')

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- INPUT CARD - Native Container, Totega nahi ---
with st.container(border=True):
    st.subheader("Nutrition Details")
    st.write("Move the sliders to match your drink's nutrition label.")

    fat = st.slider("Fat (g)", 0.0, 30.0, 2.0, 0.5)
    carb = st.slider("Carbohydrates (g)", 0.0, 100.0, 25.0, 1.0)
    protein = st.slider("Protein (g)", 0.0, 30.0, 4.0, 0.5)

    est_cal = fat*9 + carb*4 + protein*4
    st.markdown("---")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fat", f"{fat}g")
    c2.metric("Carbs", f"{carb}g")
    c3.metric("Protein", f"{protein}g")
    c4.metric("Est. Kcal", f"{est_cal:.0f}")

st.markdown("<br>", unsafe_allow_html=True)

if st.button("Predict Calorie Category →"):
    input_data = pd.DataFrame([[fat, carb, protein]], columns=['Fat (g)', 'Carb. (g)', 'Protein'])
    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]

    if prediction == 1:
        conf = proba[1]*100
        with st.container(border=True):
            st.error(f"### 🚨 High Calorie Drink")
            st.write(f"Over **150 Calories** • Model is **{conf:.1f}%** confident")
            st.caption("Tip: Try small size or skim milk")
    else:
        conf = proba[0]*100
        with st.container(border=True):
            st.success(f"### ✅ Low / Medium Calorie Drink")
            st.write(f"**150 Calories or less** • Model is **{conf:.1f}%** confident")
            st.caption("Great choice! Within moderate range")

    st.progress(int(conf))
    st.caption(f"Confidence: {conf:.1f}%")

st.markdown("---")
st.caption("Built with Python • Streamlit • Decision Tree | Final Year Project")
