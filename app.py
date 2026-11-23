import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Starbucks Calorie Predictor", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    div.stButton > button {
        width: 100% !important; border-radius: 10px !important;
        padding: 12px !important; font-weight: 700 !important; font-size: 16px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("☕ Starbucks Drink Calorie Predictor")
st.write("Predict whether your favorite Starbucks drink is **High Calorie (>150 kcal)** or **Low/Med Calorie (<=150 kcal)** based on its nutritional values.")
st.markdown("---")

@st.cache_resource
def load_model():
    return joblib.load('starbucks_decision_tree_model.joblib')

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

st.subheader("Enter Nutrition Details:")

fat = st.slider("Fat (g)", min_value=0.0, max_value=30.0, value=2.0, step=0.5)
carb = st.slider("Carbohydrates (g)", min_value=0.0, max_value=100.0, value=25.0, step=1.0)
protein = st.slider("Protein (g)", min_value=0.0, max_value=30.0, value=4.0, step=0.5)

if st.button("Predict Calorie Category", type="primary"):
    input_data = pd.DataFrame([[fat, carb, protein]], columns=['Fat (g)', 'Carb. (g)', 'Protein'])
    prediction = model.predict(input_data)[0]
    probabilities = model.predict_proba(input_data)[0]

    st.markdown("---")
    if prediction == 1:
        st.error(f"🚨 **Prediction: High Calorie (>150 Calories)**")
        st.write(f"Confidence: {probabilities[1]*100:.1f}%")
    else:
        st.success(f"✅ **Prediction: Low/Med Calorie (<=150 Calories)**")
        st.write(f"Confidence: {probabilities[0]*100:.1f}%")

    if st.button("🔄  Try Another"):
        st.rerun()

st.markdown("<p style='text-align:center; color:grey; font-size:12px; margin-top:30px;'>Starbucks Calorie Predictor • Final Year Project</p>", unsafe_allow_html=True)
