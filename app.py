import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Starbucks Calorie Predictor", page_icon="☕", layout="centered")

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

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap');
    * { font-family: 'Plus Jakarta Sans', sans-serif !important; }
    html { scroll-behavior: smooth !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header[data-testid="stHeader"] {visibility: hidden;}

    /* ===== BACKGROUND - AB NAZAR AAYEGA ===== */
    .stApp {
        background: linear-gradient(180deg, #E8F5EF 0%, #F6F9F7 35%, #FFFFFF 100%) !important;
        background-attachment: fixed !important;
    }
    .block-container {
        padding-top: 1rem !important; padding-bottom: 3rem !important; max-width: 720px !important;
    }

    /* ===== ANIMATIONS ===== */
    @keyframes fadeUp { from { opacity: 0; transform: translateY(30px) scale(0.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
    @keyframes floatLogo { 0%,100% { transform: translateY(0) rotate(0deg); } 50% { transform: translateY(-8px) rotate(2deg); } }
    @keyframes glowPulse { 0%,100% { box-shadow: 0 0 0 3px white, 0 0 0 5px #00704A, 0 15px 30px rgba(0,112,74,0.3); } 50% { box-shadow: 0 0 0 3px white, 0 0 0 5px #00A66C, 0 20px 45px rgba(0,166,108,0.5); } }
    @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
    @keyframes popIn { 0% { transform: scale(0.85); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }

    /* Hero */
    .logo-wrap { text-align: center; padding-top: 20px; animation: fadeUp 0.8s ease both; }
    .logo-circle {
        width: 96px; height: 96px; background: linear-gradient(135deg, #00704A, #00C853);
        border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto;
        animation: floatLogo 3s ease-in-out infinite, glowPulse 3s ease-in-out infinite;
    }
    .logo-s { color: white; font-size: 56px; font-weight: 800; font-family: Georgia, serif; margin-top: -4px; }
    .logo-text { font-size: 11px; font-weight: 800; letter-spacing: 5px; color: #00704A; margin-top: 12px; }
    .main-title { text-align: center; font-size: 36px; font-weight: 800; color: #111827; line-height: 1.1; margin: 14px 0 6px 0; animation: fadeUp 0.8s 0.1s ease both; }
    .main-sub { text-align: center; color: #4B5563; font-size: 15px; line-height: 1.6; animation: fadeUp 0.8s 0.2s ease both; }
    .badge { text-align:center; margin-top:14px; animation: fadeUp 0.8s 0.3s ease both; }
    .badge span {
        background: linear-gradient(90deg, #00704A, #00A66C, #00704A); background-size: 200% 100%;
        animation: shimmer 3s linear infinite;
        color: white; font-size: 11px; font-weight: 700; letter-spacing: 1px; padding: 8px 16px; border-radius: 100px;
        box-shadow: 0 4px 15px rgba(0,112,74,0.3);
    }

    /* Tabs */
    div[data-testid="stTabs"] button { font-weight: 700 !important; font-size: 15px !important; }
    div[data-testid="stTabs"] [aria-selected="true"] { color: #00704A !important; }

    /* Buttons - AB HOVER NAZAR AAYEGA */
    div.stButton > button {
        width: 100% !important; border-radius: 16px !important;
        padding: 15px 10px !important; font-weight: 700 !important; font-size: 14px !important;
        background: white !important; color: #111827 !important;
        border: 2px solid #E5E7EB !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: #00704A !important; color: white !important; border-color: #00704A !important;
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 12px 25px rgba(0,112,74,0.35) !important;
    }
    div.stButton > button:active { transform: scale(0.96) !important; }

    /* Cards - Glass + Shadow */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 22px !important; border: 1.5px solid #D1FAE5 !important;
        background: rgba(255,255,255,0.95) !important;
        box-shadow: 0 12px 35px rgba(0,112,74,0.12) !important;
        animation: fadeUp 0.8s ease both;
        transition: transform 0.3s ease !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover { transform: translateY(-3px); }

    /* Sliders */
    div[data-testid="stSlider"] [role="slider"] {
        background: #00704A !important; border: 3px solid white !important;
        box-shadow: 0 3px 10px rgba(0,112,74,0.5) !important; width: 24px !important; height: 24px !important;
    }
    .label-box { background: #F0FDF4; border: 1.5px solid #BBF7D0; border-radius: 14px; padding: 12px 14px; margin-bottom: 12px; transition: all 0.3s ease; }
    .label-box:hover { background: #DCFCE7; transform: translateX(4px); }
    .label-box b { font-size: 15px; color:#111827; }
    .label-box span { font-size: 12.5px; color: #4B5563; display:block; margin-top:2px; }

    div[data-testid="stMetric"] { background: linear-gradient(135deg, #F0FDF4, #FFFFFF); padding: 12px 8px; border-radius: 14px; border: 1.5px solid #BBF7D0; text-align:center; animation: popIn 0.5s ease both; }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] { font-size: 21px !important; color: #00704A !important; }

    /* Result */
    .result-high { background: linear-gradient(135deg, #FEF2F2, #FFF7ED); border: 2px solid #FCA5A5; border-radius: 20px; padding: 24px; text-align: center; animation: popIn 0.6s ease both; box-shadow: 0 10px 30px rgba(220,38,38,0.15); }
    .result-low { background: linear-gradient(135deg, #F0FDF4, #ECFDF5); border: 2px solid #86EFAC; border-radius: 20px; padding: 24px; text-align: center; animation: popIn 0.6s ease both; box-shadow: 0 10px 30px rgba(22,163,74,0.15); }
    .result-high h3 { color:#DC2626; margin:0; font-size:24px; }
    .result-low h3 { color:#16A34A; margin:0; font-size:24px; }
    .result-sub { color:#4B5563; font-size:14px; margin-top:10px; line-height:1.7; }

    /* Meter */
    .meter-wrap { background: linear-gradient(135deg, #FFFFFF, #F0FDF4); border: 1.5px solid #BBF7D0; border-radius: 18px; padding: 18px; margin-top: 16px; box-shadow: 0 6px 20px rgba(0,112,74,0.08); animation: fadeUp 0.8s ease both; }
    .meter-top { display:flex; justify-content:space-between; align-items:center; }
    .meter-title { font-weight: 800; font-size: 14px; color:#111827; }
    .meter-val { font-weight: 800; font-size: 22px; }
    .meter-bar-bg { background: #E5E7EB; height: 14px; border-radius: 100px; overflow:hidden; margin-top:12px; }
    .meter-bar { height:100%; border-radius:100px; transition: width 0.8s ease; }
    .meter-labels { display:flex; justify-content:space-between; font-size:11px; color:#6B7280; font-weight:600; margin-top:6px; }
    .meter-status { text-align:center; font-size:13.5px; font-weight:700; margin-top:12px; }
    div[data-testid="stDataFrame"] { border-radius: 16px; overflow: hidden; border: 1.5px solid #BBF7D0; box-shadow: 0 8px 25px rgba(0,0,0,0.06); }
    div[data-testid="stAlert"] { border-radius: 14px !important; }
    div[data-testid="stProgress"] > div > div > div { background: linear-gradient(90deg, #00704A, #00C853) !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""<div class="logo-wrap"><div class="logo-circle"><div class="logo-s">S</div></div><div class="logo-text">STARBUCKS</div></div>""", unsafe_allow_html=True)
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
    st.markdown('<h3 style="margin-bottom:2px;">⚡ Try Example Drinks</h3><p style="color:#6B7280; font-size:13px; margin-top:0;">One click - values will set automatically</p>', unsafe_allow_html=True)
    e1, e2, e3 = st.columns(3)
    with e1: st.button("☕ Black Coffee", on_click=set_drink, args=(0.0, 2.0, 1.0))
    with e2: st.button("🥛 Skinny Latte", on_click=set_drink, args=(1.0, 18.0, 10.0))
    with e3: st.button("🍫 Frappuccino", on_click=set_drink, args=(12.0, 65.0, 5.0))
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
        pct = min(est / 400 * 100, 100)
        if est <= 150:
            m_color = "#16A34A"; m_status = "✅ Low / Medium Zone - Safe Choice"; m_text_color = "#16A34A"
        elif est <= 250:
            m_color = "#F59E0B"; m_status = "⚠️ Medium-High Zone - Be Careful"; m_text_color = "#D97706"
        else:
            m_color = "#DC2626"; m_status = "🚨 High Calorie Zone - Heavy Drink"; m_text_color = "#DC2626"
        st.markdown(f"""
        <div class="meter-wrap">
            <div class="meter-top"><div class="meter-title">🔥 Live Calorie Meter</div><div class="meter-val" style="color:{m_text_color};">{est:.0f} kcal</div></div>
            <div class="meter-bar-bg"><div class="meter-bar" style="width:{pct:.0f}%; background:{m_color};"></div></div>
            <div class="meter-labels"><span>0</span><span>150 • Limit</span><span>250</span><span>400+</span></div>
            <div class="meter-status" style="color:{m_text_color};">{m_status}</div>
        </div>
        """, unsafe_allow_html=True)
    st.write("")
    if st.button("Predict Calorie Category  →"):
        data = pd.DataFrame([[fat, carb, protein]], columns=['Fat (g)', 'Carb. (g)', 'Protein'])
        pred = model.predict(data)[0]
        proba = model.predict_proba(data)[0]
        conf = max(proba)*100
        st.write("")
        if pred == 1:
            st.markdown(f"""<div class="result-high"><h3>🚨 High Calorie Drink</h3><div class="result-sub">Your drink has <b>more than 150 Calories</b>.<br>Model Confidence: <b>{conf:.1f}%</b> • Estimated: <b>{est:.0f} kcal</b><br>💡 Tip: Try a small size, skim milk or less syrup.</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="result-low"><h3>✅ Low / Medium Calorie Drink</h3><div class="result-sub">Your drink has <b>150 Calories or less</b>.<br>Model Confidence: <b>{conf:.1f}%</b> • Estimated: <b>{est:.0f} kcal</b><br>💡 Great choice! This is in a moderate calorie range.</div></div>""", unsafe_allow_html=True)
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
st.markdown('<p style="text-align:center; color:#6B7280; font-size:12px;">Built with Python • Streamlit • Decision Tree | Final Year Project</p>', unsafe_allow_html=True)
