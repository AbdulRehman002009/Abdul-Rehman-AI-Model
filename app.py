import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Starbucks Calorie Predictor", page_icon="☕", layout="centered")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .block-container { padding-top: 1.8rem !important; max-width: 700px !important; }

    /* LOGO */
    .logo-circle {
        width: 72px; height: 72px; background: #00704A;
        border-radius: 50%; display: flex; align-items: center;
        justify-content: center; font-size: 36px;
        box-shadow: 0 8px 20px rgba(0,112,74,0.30);
        margin: 0 auto;
    }
    .main-title {
        text-align: center; font-size: 34px; font-weight: 800;
        line-height: 1.1; margin: 16px 0 6px 0; color: #111827;
    }
    .main-sub {
        text-align: center; color: #6B7280; font-size: 15px; line-height: 1.5;
    }
    .badge {
        display: block; text-align: center; margin-top: 10px;
    }
    .badge span {
        background: #E8F5EF; color: #00704A; font-size: 11px; font-weight: 700;
        letter-spacing: 1px; padding: 6px 12px; border-radius: 100px;
    }
    /* BUTTON - PRO */
    div.stButton > button {
        width: 100% !important; border-radius: 12px !important;
        padding: 15px !important; font-weight: 700 !important; font-size: 16px !important;
        background: #00704A !important; color: white !important; border: none !important;
        box-shadow: 0 6px 18px rgba(0,112,74,0.25) !important;
    }
    div.stButton > button:hover { background: #005A3C !important; transform: translateY(-1px); }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER WITH LOGO ----------
st.markdown('<div class="logo-circle">☕</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">Starbucks Drink<br>Calorie Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Check if your favourite Starbucks drink is<br><b>High Calorie</b> or <b>Low / Medium Calorie</b></div>', unsafe_allow_html=True)
st.markdown('<div class="badge"><span>● MACHINE LEARNING • DECISION TREE MODEL</span></div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load('starbucks_decision_tree_model.joblib')

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# ---------- BODY CARD ----------
with st.container(border=True):
    st.markdown("### 🥤 Nutrition Details")
    st.caption("Move the sliders to match your drink's nutrition label.")

    fat = st.slider("Fat (g)", 0.0, 30.0, 2.0, 0.5)
    carb = st.slider("Carbohydrates (g)", 0.0, 100.0, 25.0, 1.0)
    protein = st.slider("Protein (g)", 0.0, 30.0, 4.0, 0.5)

    est = fat*9 + carb*4 + protein*4
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fat", f"{fat}g")
    c2.metric("Carbs", f"{carb}g")
    c3.metric("Protein", f"{protein}g")
    c4.metric("Est. Kcal", f"{est:.0f}")

st.write("")

# ---------- PREDICT BUTTON ----------
if st.button("Predict Calorie Category  →"):
    data = pd.DataFrame([[fat, carb, protein]], columns=['Fat (g)', 'Carb. (g)', 'Protein'])
    pred = model.predict(data)[0]
    proba = model.predict_proba(data)[0]
    conf = max(proba)*100

    st.write("")
    if pred == 1:
        with st.container(border=True):
            st.markdown('<h3 style="color:#DC2626; margin:0;">🚨 High Calorie Drink</h3>', unsafe_allow_html=True)
            st.write(f"Your drink has **more than 150 Calories**.")
            st.write(f"Model Confidence: **{conf:.1f}%**")
            st.info("💡 Tip: Try a small size, skim milk or less syrup.")
    else:
        with st.container(border=True):
            st.markdown('<h3 style="color:#16A34A; margin:0;">✅ Low / Medium Calorie Drink</h3>', unsafe_allow_html=True)
            st.write(f"Your drink has **150 Calories or less**.")
            st.write(f"Model Confidence: **{conf:.1f}%**")
            st.info("💡 Great choice! This is in a moderate calorie range.")

    st.progress(int(conf))

st.markdown("---")
st.markdown('<p style="text-align:center; color:#9CA3AF; font-size:12px;">Built with Python • Streamlit • Decision Tree | Final Year Project</p>', unsafe_allow_html=True)
