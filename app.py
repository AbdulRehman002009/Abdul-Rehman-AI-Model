import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Starbucks Calorie Predictor", page_icon="☕", layout="centered")

# ---------- PRO MODERN CSS ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;}
    .block-container { max-width: 720px !important; padding-top: 2.5rem !important; }

    .top-badge {
        display: inline-block; background: #E8F5EF; color: #00704A;
        font-size: 12px; font-weight: 700; letter-spacing: 0.8px;
        padding: 6px 12px; border-radius: 100px; text-transform: uppercase;
    }
    .subtitle { color: #6B7280; font-size: 15px; line-height: 1.6; margin-top: 8px; }
    .card {
        background: white; border: 1px solid #EDEDED; border-radius: 16px;
        padding: 22px; box-shadow: 0 4px 20px rgba(0,0,0,0.04);
    }
    .mini-card {
        background: #F9FAFB; border: 1px solid #F0F0F0; border-radius: 12px;
        padding: 14px; text-align: center;
    }
    .mini-card b { font-size: 20px; display: block; }
    .mini-card span { font-size: 12px; color: #6B7280; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    div.stButton > button {
        width: 100% !important; border-radius: 12px !important; padding: 14px !important;
        font-weight: 700 !important; font-size: 16px !important;
        background: #111827 !important; color: white !important; border: none !important;
        box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    }
    div.stButton > button:hover { background: #000000 !important; }
</style>
""", unsafe_allow_html=True)

# ---------- HEADER ----------
st.markdown('<span class="top-badge">● Machine Learning • Decision Tree</span>', unsafe_allow_html=True)
st.markdown('<h1 style="font-size:36px; font-weight:800; line-height:1.1; margin:14px 0 0 0;">Starbucks Drink<br>Calorie Predictor</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter your drink\'s nutrition values and instantly check if it\'s a <b>High Calorie</b> or <b>Low / Medium Calorie</b> choice.</p>', unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load('starbucks_decision_tree_model.joblib')

try:
    model = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# ---------- INPUT CARD ----------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<p style="font-weight:700; font-size:16px; margin:0 0 16px 0;">Nutrition Details</p>', unsafe_allow_html=True)

fat = st.slider("Fat (g)", 0.0, 30.0, 2.0, 0.5)
carb = st.slider("Carbohydrates (g)", 0.0, 100.0, 25.0, 1.0)
protein = st.slider("Protein (g)", 0.0, 30.0, 4.0, 0.5)

est_cal = fat*9 + carb*4 + protein*4
st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="mini-card"><b>{fat}g</b><span>Fat</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="mini-card"><b>{carb}g</b><span>Carbs</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="mini-card"><b>{protein}g</b><span>Protein</span></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="mini-card" style="background:#111827; border-color:#111827;"><b style="color:white;">{est_cal:.0f}</b><span style="color:#D1D5DB;">Est. Kcal</span></div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ---------- PREDICT ----------
if st.button("Predict Calorie Category →"):
    input_data = pd.DataFrame([[fat, carb, protein]], columns=['Fat (g)', 'Carb. (g)', 'Protein'])
    prediction = model.predict(input_data)[0]
    proba = model.predict_proba(input_data)[0]

    st.markdown("<br>", unsafe_allow_html=True)
    if prediction == 1:
        conf = proba[1]*100
        st.markdown(f"""
        <div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:16px; padding:22px; display:flex; gap:16px; align-items:center;">
            <div style="font-size:38px;">🚨</div>
            <div><div style="font-weight:800; font-size:19px; color:#991B1B;">High Calorie Drink</div>
            <div style="color:#6B7280; font-size:14px; margin-top:4px;">Over <b>150 Calories</b> • Model is <b>{conf:.1f}%</b> confident</div>
            <div style="background:#FEE2E2; color:#991B1B; font-size:12px; font-weight:700; padding:5px 10px; border-radius:100px; display:inline-block; margin-top:10px;">TIP: TRY SMALL SIZE OR SKIM MILK</div></div>
        </div>""", unsafe_allow_html=True)
    else:
        conf = proba[0]*100
        st.markdown(f"""
        <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:16px; padding:22px; display:flex; gap:16px; align-items:center;">
            <div style="font-size:38px;">✅</div>
            <div><div style="font-weight:800; font-size:19px; color:#166534;">Low / Medium Calorie Drink</div>
            <div style="color:#6B7280; font-size:14px; margin-top:4px;"><b>150 Calories or less</b> • Model is <b>{conf:.1f}%</b> confident</div>
            <div style="background:#DCFCE7; color:#166534; font-size:12px; font-weight:700; padding:5px 10px; border-radius:100px; display:inline-block; margin-top:10px;">GREAT CHOICE • WITHIN MODERATE RANGE</div></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:13px; color:#6B7280; margin:0;">Confidence: <b>{conf:.1f}%</b></p>', unsafe_allow_html=True)
    st.progress(int(conf))

st.markdown("---")
st.markdown('<p style="text-align:center; color:#9CA3AF; font-size:12px;">Built with Python • Streamlit • Decision Tree &nbsp;|&nbsp; Final Year Project</p>', unsafe_allow_html=True)
