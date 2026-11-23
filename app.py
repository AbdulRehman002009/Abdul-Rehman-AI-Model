import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Starbucks Calorie Predictor", page_icon="☕", layout="centered")

# --- Session State for Example Buttons ---
if 'fat' not in st.session_state:
    st.session_state.fat = 2.0
if 'carb' not in st.session_state:
    st.session_state.carb = 25.0
if 'protein' not in st.session_state:
    st.session_state.protein = 4.0

st.markdown("""
<style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .block-container { padding-top: 1.5rem !important; max-width: 700px !important; }
    .logo-wrap { text-align: center; margin-bottom: 8px; }
    .logo-circle {
        width: 84px; height: 84px; background: #00704A;
        border-radius: 50%; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        margin: 0 auto; border: 3px solid #FFFFFF;
        box-shadow: 0 0 0 2px #00704A, 0 10px 22px rgba(0,112,74,0.30);
    }
    .logo-s { color: white; font-size: 38px; font-weight: 800; line-height: 1; font-family: Georgia, serif; }
    .logo-star { color: white; font-size: 11px; letter-spacing: 4px; margin-top: 2px; }
    .logo-text { font-size: 11px; font-weight: 800; letter-spacing: 3px; color: #00704A; margin-top: 10px; }
    .main-title { text-align: center; font-size: 32px; font-weight: 800; color: #111827; line-height: 1.15; margin: 12px 0 6px 0; }
    .main-sub { text-align: center; color: #6B7280; font-size: 15px; line-height: 1.5; }
    div.stButton > button {
        width: 100% !important; border-radius: 12px !important;
        padding: 15px !important; font-weight: 700 !important; font-size: 16px !important;
        background: #00704A !important; color: white !important; border: none !important;
        box-shadow: 0 6px 18px rgba(0,112,74,0.25) !important;
    }
    div.stButton > button:hover { background: #005A3C !important; }
    div[data-testid="stSlider"] > div > div > div > div { background: #E5E7EB !important; }
    div[data-testid="stSlider"] [role="slider"] {
        background: #111827 !important; border: 2px solid white !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.25) !important;
        width: 20px !important; height: 20px !important;
    }
    .label-box { background: #F9FAFB; border: 1px solid #EDEDED; border-radius: 10px; padding: 10px 12px; margin-bottom: 14px; }
    .label-box b { font-size: 14px; }
    .label-box span { font-size: 12px; color: #6B7280; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="logo-wrap">
    <div class="logo-circle">
        <div class="logo-star">★ ★ ★</div>
        <div class="logo-s">S</div>
        <div class="logo-star">★ ★ ★</div>
    </div>
    <div class="logo-text">STARBUCKS</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Drink Calorie Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Check if your favourite Starbucks drink is<br><b>High Calorie</b> or <b>Low / Medium Calorie</b></div>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; margin-top:10px;"><span style="background:#E8F5EF; color:#00704A; font-size:11px; font-weight:700; letter-spacing:1px; padding:6px 12px; border-radius:100px;">● MACHINE LEARNING • DECISION TREE</span></p>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load('starbucks_decision_tree_model.joblib')

model = load_model()

# ---------- EXAMPLE BUTTONS ----------
st.markdown("### ⚡ Try Example Drinks")
st.caption("One click - values will set automatically")
e1, e2, e3 = st.columns(3)
with e1:
    if st.button("☕ Black Coffee"):
        st.session_state.fat = 0.0
        st.session_state.carb = 2.0
        st.session_state.protein = 1.0
        st.rerun()
with e2:
    if st.button("🥛 Skinny Latte"):
        st.session_state.fat = 1.0
        st.session_state.carb = 18.0
        st.session_state.protein = 10.0
        st.rerun()
with e3:
    if st.button("🍫 Frappuccino"):
        st.session_state.fat = 12.0
        st.session_state.carb = 65.0
        st.session_state.protein = 5.0
        st.rerun()

st.write("")

# ---------- BODY ----------
with st.container(border=True):
    st.markdown("### 🥤 Nutrition Details")
    st.caption("Select values from your drink's nutrition label.")

    st.markdown('<div class="label-box"><b>🧈 Fat (g)</b><br><span>Fat makes drinks creamy but adds most calories — 1g Fat = 9 kcal</span></div>', unsafe_allow_html=True)
    fat = st.slider("Fat (g)", 0.0, 30.0, key="fat", label_visibility="collapsed")

    st.markdown('<div class="label-box"><b>🍞 Carbohydrates (g)</b><br><span>Sugar & syrups come here — 1g Carb = 4 kcal</span></div>', unsafe_allow_html=True)
    carb = st.slider("Carbohydrates (g)", 0.0, 100.0, key="carb", label_visibility="collapsed")

    st.markdown('<div class="label-box"><b>🥛 Protein (g)</b><br><span>Comes from milk — 1g Protein = 4 kcal</span></div>', unsafe_allow_html=True)
    protein = st.slider("Protein (g)", 0.0, 30.0, key="protein", label_visibility="collapsed")

    est = fat*9 + carb*4 + protein*4
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Fat", f"{fat}g")
    c2.metric("Carbs", f"{carb}g")
    c3.metric("Protein", f"{protein}g")
    c4.metric("Est. Kcal", f"{est:.0f}")

    # Reset Button
    if st.button("🔄 Reset All"):
        st.session_state.fat = 2.0
        st.session_state.carb = 25.0
        st.session_state.protein = 4.0
        st.rerun()

st.write("")

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
