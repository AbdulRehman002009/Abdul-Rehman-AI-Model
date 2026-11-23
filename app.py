import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Starbucks Calorie Predictor", page_icon="☕", layout="centered")

# ---------- FIX: Callback Functions ----------
def set_drink(f, c, p):
    st.session_state.fat = f
    st.session_state.carb = c
    st.session_state.protein = p

def reset_all():
    st.session_state.fat = 2.0
    st.session_state.carb = 25.0
    st.session_state.protein = 4.0

if 'fat' not in st.session_state:
    st.session_state.fat = 2.0
if 'carb' not in st.session_state:
    st.session_state.carb = 25.0
if 'protein' not in st.session_state:
    st.session_state.protein = 4.0

# ---------- TOP LEVEL PREMIUM DESIGN ----------
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    html { scroll-behavior: smooth !important; }
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {visibility: hidden;}

    .block-container { padding-top: 1rem !important; padding-bottom: 2rem !important; max-width: 720px !important; }

    /* Animation */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(18px); }
        to { opacity: 1; transform: translateY(0); }
    }
    @keyframes floatLogo {
        0%,100% { transform: translateY(0px); }
        50% { transform: translateY(-6px); }
    }
    @keyframes pulseGlow {
        0%,100% { box-shadow: 0 0 0 2px #00704A, 0 10px 25px rgba(0,112,74,0.30); }
        50% { box-shadow: 0 0 0 2px #00704A, 0 14px 35px rgba(0,112,74,0.45); }
    }
    .anim { animation: fadeUp 0.7s ease both; }
    .anim2 { animation: fadeUp 0.7s ease 0.15s both; }
    .anim3 { animation: fadeUp 0.7s ease 0.3s both; }

    /* Hero */
    .logo-wrap { text-align: center; margin-bottom: 6px; padding-top: 18px; animation: fadeUp 0.7s ease both; }
    .logo-circle {
        width: 92px; height: 92px; background: linear-gradient(135deg, #00704A, #00A66C);
        border-radius: 50%; display: flex;
        align-items: center; justify-content: center;
        margin: 0 auto;
        border: 3px solid #FFFFFF;
        animation: floatLogo 3s ease-in-out infinite, pulseGlow 3s ease-in-out infinite;
        overflow: hidden;
    }
    .logo-s { color: white; font-size: 54px; font-weight: 800; line-height: 1; font-family: Georgia, serif; margin-top: -4px; }
    .logo-text { font-size: 11px; font-weight: 800; letter-spacing: 4px; color: #00704A; margin-top: 10px; }
    .main-title { text-align: center; font-size: 34px; font-weight: 800; color: #111827; line-height: 1.12; margin: 12px 0 6px 0; }
    .main-sub { text-align: center; color: #6B7280; font-size: 15px; line-height: 1.6; }
    .badge { text-align:center; margin-top:12px; }
    .badge span { background:#E8F5EF; color:#00704A; font-size:11px; font-weight:700; letter-spacing:1px; padding:7px 14px; border-radius:100px; border:1px solid #C8E6D5; }

    /* Tabs */
    div[data-testid="stTabs"] button { font-weight: 700 !important; font-size: 15px !important; }
    div[data-testid="stTabs"] [data-baseweb="tab-list"] { gap: 8px; }
    div[data-testid="stTabs"] [aria-selected="true"] { color: #00704A !important; }

    /* Buttons - Example Drinks */
    div.stButton > button {
        width: 100% !important; border-radius: 14px !important;
        padding: 14px 10px !important; font-weight: 700 !important; font-size: 14px !important;
        background: white !important; color: #111827 !important;
        border: 1.5px solid #E5E7EB !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
        transition: all 0.25s ease !important;
    }
    div.stButton > button:hover {
        background: #00704A !important; color: white !important; border-color: #00704A !important;
        transform: translateY(-2px); box-shadow: 0 8px 20px rgba(0,112,74,0.25) !important;
    }
    div.stButton > button:active { transform: translateY(0px) scale(0.98); }

    /* Main Predict Button - special */
    div[data-testid="stVerticalBlock"] > div:has(> div > button) { animation: fadeUp 0.7s ease both; }

    /* Cards */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 20px !important;
        border: 1px solid #EDEDED !important;
        box-shadow: 0 8px 30px rgba(0,0,0,0.06) !important;
        animation: fadeUp 0.7s ease both;
    }

    /* Sliders */
    div[data-testid="stSlider"] > div > div > div > div { background: #E5E7EB !important; }
    div[data-testid="stSlider"] [role="slider"] {
        background: #00704A !important; border: 2.5px solid white !important;
        box-shadow: 0 2px 8px rgba(0,112,74,0.4) !important;
        width: 22px !important; height: 22px !important;
    }

    .label-box { background: #F9FAFB; border: 1px solid #EDEDED; border-radius: 12px; padding: 11px 13px; margin-bottom: 12px; transition: all 0.2s ease; }
    .label-box:hover { background: #EFFAF4; border-color: #C8E6D5; }
    .label-box b { font-size: 14.5px; color:#111827; }
    .label-box span { font-size: 12.5px; color: #6B7280; line-height:1.5; display:block; margin-top:2px; }

    /* Metrics */
    div[data-testid="stMetric"] { background: #F9FAFB; padding: 10px 8px; border-radius: 12px; border: 1px solid #EDEDED; text-align:center; }
    div[data-testid="stMetric"] label { font-size: 12px !important; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { font-size: 20px !important; color: #00704A !important; }

    /* Result Box */
    .result-high {
        background: linear-gradient(135deg, #FEF2F2, #FFF7ED);
        border: 1.5px solid #FECACA; border-radius: 18px; padding: 20px;
        text-align: center; animation: fadeUp 0.6s ease both;
    }
    .result-low {
        background: linear-gradient(135deg, #F0FDF4, #ECFDF5);
        border: 1.5px solid #BBF7D0; border-radius: 18px; padding: 20px;
        text-align: center; animation: fadeUp 0.6s ease both;
    }
    .result-high h3 { color:#DC2626; margin:0; font-size:22px; }
    .result-low h3 { color:#16A34A; margin:0; font-size:22px; }
    .result-sub { color:#4B5563; font-size:14px; margin-top:8px; line-height:1.6; }

    /* Dataframe */
    div[data-testid="stDataFrame"] { border-radius: 16px; overflow: hidden; border: 1px solid #EDEDED; }

    /* Info boxes */
    div[data-testid="stAlert"] { border-radius: 14px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="logo-wrap">
    <div class="logo-circle">
        <div class="logo-s">S</div>
    </div>
    <div class="logo-text">STARBUCKS</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">Drink Calorie Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Check if your favourite Starbucks drink is<br><b>High Calorie</b> or <b>Low / Medium Calorie</b></div>', unsafe_allow_html=True)
st.markdown('<div class="badge"><span>● MACHINE LEARNING • DECISION TREE</span></div>', unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    return joblib.load('starbucks_decision_tree_model.joblib')

model = load_model()

tab1, tab2 = st.tabs(["🔮 Predict Calories", "📖 Starbucks Menu"])

with tab1:
    st.markdown('<div class="anim"><h3 style="margin-bottom:2px;">⚡ Try Example Drinks</h3><p style="color:#6B7280; font-size:13px; margin-top:0;">One click - values will set automatically</p></div>', unsafe_allow_html=True)
    e1, e2, e3 = st.columns(3)
    with e1:
        st.button("☕ Black Coffee", on_click=set_drink, args=(0.0, 2.0, 1.0))
    with e2:
        st.button("🥛 Skinny Latte", on_click=set_drink, args=(1.0, 18.0, 10.0))
    with e3:
        st.button("🍫 Frappuccino", on_click=set_drink, args=(12.0, 65.0, 5.0))
    st.write("")
    with st.container(border=True):
        st.markdown("### 🥤 Nutrition Details")
        st.caption("Select values from your drink's nutrition label.")
        st.markdown('<div class="label-box"><b>🧈 Fat (g)</b><span>Fat makes drinks creamy but adds most calories — 1g Fat = 9 kcal</span></div>', unsafe_allow_html=True)
        fat = st.slider("Fat (g)", 0.0, 30.0, key="fat", label_visibility="collapsed")
        st.markdown('<div class="label-box"><b>🍞 Carbohydrates (g)</b><span>Sugar & syrups come here — 1g Carb = 4 kcal</span></div>', unsafe_allow_html=True)
        carb = st.slider("Carbohydrates (g)", 0.0, 100.0, key="carb", label_visibility="collapsed")
        st.markdown('<div class="label-box"><b>🥛 Protein (g)</b><span>Comes from milk — 1g Protein = 4 kcal</span></div>', unsafe_allow_html=True)
        protein = st.slider("Protein (g)", 0.0, 30.0, key="protein", label_visibility="collapsed")
        est = fat*9 + carb*4 + protein*4
        st.divider()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Fat", f"{fat:.0f}g")
        c2.metric("Carbs", f"{carb:.0f}g")
        c3.metric("Protein", f"{protein:.0f}g")
        c4.metric("Est. Kcal", f"{est:.0f}")
        st.button("🔄 Reset All", on_click=reset_all)
    st.write("")
    if st.button("Predict Calorie Category  →"):
        data = pd.DataFrame([[fat, carb, protein]], columns=['Fat (g)', 'Carb. (g)', 'Protein'])
        pred = model.predict(data)[0]
        proba = model.predict_proba(data)[0]
        conf = max(proba)*100
        st.write("")
        if pred == 1:
            st.markdown(f"""
            <div class="result-high">
                <h3>🚨 High Calorie Drink</h3>
                <div class="result-sub">Your drink has <b>more than 150 Calories</b>.<br>Model Confidence: <b>{conf:.1f}%</b><br>💡 Tip: Try a small size, skim milk or less syrup.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-low">
                <h3>✅ Low / Medium Calorie Drink</h3>
                <div class="result-sub">Your drink has <b>150 Calories or less</b>.<br>Model Confidence: <b>{conf:.1f}%</b><br>💡 Great choice! This is in a moderate calorie range.</div>
            </div>
            """, unsafe_allow_html=True)
        st.write("")
        st.progress(int(conf))

with tab2:
    st.markdown("### 📖 Starbucks Menu Reference")
    st.caption("Don't know a drink? Check here first, then go to Predict tab.")
    menu = pd.DataFrame([
        ["☕ Black Coffee", "Just coffee, no milk/sugar", 5, "Low"],
        ["🍵 Green Tea Latte", "Green tea + steamed milk", 120, "Low"],
        ["🥛 Caffe Latte", "Espresso + steamed milk", 150, "Low / Medium"],
        ["🤎 Cappuccino", "Espresso + milk foam", 120, "Low"],
        ["🤍 Skinny Latte", "Non-fat milk + sugar-free syrup", 100, "Low"],
        ["🍯 Caramel Macchiato", "Vanilla + milk + caramel", 180, "High"],
        ["🍫 Mocha Frappuccino", "Coffee + chocolate + cream", 370, "High"],
        ["🍓 Strawberry Frappuccino", "Strawberry + milk + cream", 300, "High"],
        ["🧋 Iced White Mocha", "White chocolate + milk + ice", 260, "High"],
        ["🥤 Cold Brew", "Slow-steeped cold coffee", 10, "Low"],
    ], columns=["Drink Name", "What is it?", "Approx. Calories", "Category"])
    st.dataframe(menu, use_container_width=True, hide_index=True)
    st.info("💡 Tip: Menu se drink dekh kar, Predict wale tab me uski values daal kar check karo.")

st.markdown("---")
st.markdown('<p style="text-align:center; color:#9CA3AF; font-size:12px;">Built with Python • Streamlit • Decision Tree | Final Year Project</p>', unsafe_allow_html=True)
