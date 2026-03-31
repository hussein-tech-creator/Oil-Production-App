import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# 1. إعدادات الصفحة (تصميم نظيف ومريح للعين)
st.set_page_config(page_title="Petro-Elite Dashboard", layout="wide", page_icon="🛢️")

st.markdown("""
    <style>
    /* خلفية بيضاء ساطعة */
    .stApp { background-color: #ffffff; }
    
    /* تنسيق القائمة الجانبية بلون أزرق بترولي فاتح */
    section[data-testid="stSidebar"] {
        background-color: #f0f4f8;
        border-right: 2px solid #d1d9e6;
    }
    
    /* وضوح النصوص في القائمة الجانبية */
    section[data-testid="stSidebar"] .css-17l2qt2 { color: #003366; }
    
    /* بطاقات النتائج (Metrics) بشكل بارز ونظيف */
    div[data-testid="stMetric"] {
        background-color: #f8fbff;
        border: 2px solid #e1e8f0;
        padding: 20px;
        border-radius: 10px;
    }
    
    /* تنسيق العناوين */
    h1, h2, h3 { color: #003366; font-family: 'Arial', sans-serif; }
    
    .logo-container {
        text-align: center;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية (شعار نفطي حقيقي + وضوح عالٍ)
with st.sidebar:
    # شعار صناعي (أيقونة مصفاة/بئر نفط)
    logo_url = "https://cdn-icons-png.flaticon.com/512/2518/2518048.png"
    st.markdown(f'<div class="logo-container"><img src="{logo_url}" width="130"></div>', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>Asset Management</h3>", unsafe_allow_html=True)
    st.write("---")
    
    # تنظيم المدخلات بشكل مريح
    st.subheader("🛠️ Reservoir Parameters")
    p_res = st.number_input("Reservoir Pressure (psi)", value=3500)
    pi = st.slider("Productivity Index (J)", 0.5, 5.0, 1.5)
    
    st.subheader("💰 Economic Factors")
    oil_price = st.slider("Oil Price ($/bbl)", 40, 140, 85)
    t_size = st.selectbox("Tubing Size (in)", [2.375, 2.875, 3.5])

# 3. محرك الحسابات (Nodal Analysis)
q_range = np.linspace(0, p_res * pi, 100)
pwf_ipr = p_res - (q_range / pi)
# معادلة VLP محسنة هندسياً
pwf_vlp = 200 + (0.0008 * q_range**1.8 / (t_size/2.875)**4) + 1100

idx = np.argwhere(np.diff(np.sign(pwf_ipr - pwf_vlp))).flatten()
opt_q = q_range[idx[0]] if len(idx) > 0 else 0
opt_p = pwf_ipr[idx[0]] if len(idx) > 0 else 0

# 4. واجهة النتائج الرئيسية
st.title("💎 Petro-Elite™ Production Optimizer")
st.write("Engineering Intelligence for Field Development")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Optimal Rate", f"{int(opt_q)} bbl/d", delta="Stabilized")
with col2:
    st.metric("Operating Pressure", f"{int(opt_p)} psi")
with col3:
    st.metric("Daily Revenue", f"${int(opt_q * oil_price):,}")

st.markdown("---")

# 5. الرسم البياني (ألوان واضحة جداً)
st.subheader("📊 Production Optimization Plot (Nodal Analysis)")
fig = go.Figure()

# منحنى الخزان (IPR) باللون الأزرق
fig.add_trace(go.Scatter(x=q_range, y=pwf_ipr, name="Inflow (IPR)", 
                         line=dict(color='#0056b3', width=4)))
# منحنى البئر (VLP) باللون الأحمر الواضح
fig.add_trace(go.Scatter(x=q_range, y=pwf_vlp, name="Outflow (VLP)", 
                         line=dict(color='#d9534f', width=4)))

if opt_q > 0:
    fig.add_trace(go.Scatter(x=[opt_q], y=[opt_p], mode='markers', name="Operating Point",
                             marker=dict(size=15, color='#ffcc00', line=dict(width=2, color='black'))))

fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    xaxis=dict(gridcolor='#e5e5e5', title="Production Rate (bbl/d)"),
    yaxis=dict(gridcolor='#e5e5e5', title="Pressure (psi)"),
    height=500,
    legend=dict(x=0.7, y=0.9)
)
st.plotly_chart(fig, use_container_width=True)

# 6. تذييل الصفحة
st.info(f"Analysis Summary: Current Tubing ({t_size}\") is providing an optimal match at {int(opt_q)} bbl/d.")
st.markdown(f"<p style='text-align: center; color: gray;'>Developed by Eng. Hussein Ali | Petroleum Engineering Excellence 2026</p>", unsafe_allow_html=True)
