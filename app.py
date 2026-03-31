import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# 1. إعدادات الصفحة والتصميم الفاخر
st.set_page_config(page_title="Petro-Elite Optimizer", layout="wide", page_icon="🛢️")

st.markdown("""
    <style>
    /* تغيير لون الخلفية العام */
    .stApp { background-color: #f4f7f9; }
    
    /* تنسيق البطاقات العلوية */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e0e6ed;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03);
    }
    
    /* تنسيق القائمة الجانبية */
    section[data-testid="stSidebar"] {
        background-color: #1e293b;
        color: white;
    }
    
    /* تنسيق العنوان */
    h1 { color: #0f172a; font-family: 'Segoe UI', sans-serif; font-weight: 700; }
    
    /* لوحة التحكم الجانبية */
    .sidebar-logo {
        display: flex;
        justify-content: center;
        padding: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية مع الشعار الجديد
with st.sidebar:
    # تم تغيير الرابط لشعار يعبر عن الطاقة والتقنية (قطرة نفط تقنية)
    logo_url = "https://cdn-icons-png.flaticon.com/512/4114/4114944.png"
    st.markdown(f'<div class="sidebar-logo"><img src="{logo_url}" width="110"></div>', unsafe_allow_html=True)
    
    st.markdown("<h2 style='text-align: center; color: white;'>Asset Control</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Eng. Hussein Ali Al-Amery</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    tab_eng, tab_econ = st.tabs(["⚙️ Physics", "💰 Market"])
    
    with tab_eng:
        p_res = st.number_input("Res. Pressure (psi)", value=3500, help="Reservoir static pressure")
        pi = st.slider("Productivity Index (J)", 0.5, 5.0, 1.5)
        t_size = st.selectbox("Tubing Size (inch)", [2.375, 2.875, 3.5])
    
    with tab_econ:
        oil_price = st.slider("Oil Price ($/bbl)", 40, 140, 85)
        opex = st.number_input("Lifting Cost ($/bbl)", value=15)

# 3. الحسابات الهندسية (Nodal Analysis)
q_range = np.linspace(0, p_res * pi, 50)
pwf_ipr = p_res - (q_range / pi)
pwf_vlp = 250 + (0.0007 * q_range**2 / (t_size/2.875)**4) + 1000

idx = np.argwhere(np.diff(np.sign(pwf_ipr - pwf_vlp))).flatten()
opt_q = q_range[idx[0]] if len(idx) > 0 else 0
opt_p = pwf_ipr[idx[0]] if len(idx) > 0 else 0

# 4. لوحة القيادة (Dashboard)
st.title("💎 Petro-Elite Optimizer")
st.write("Advanced Nodal Analysis & Production Maximization")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Optimal Flow Rate", f"{int(opt_q)} bbl/d")
m2.metric("Flowing Pressure", f"{int(opt_p)} psi")
m3.metric("Daily Net Profit", f"${int(opt_q * (oil_price - opex)):,}")
m4.metric("Asset Efficiency", f"{int((opt_q/(p_res*pi))*100)}%")

# 5. التحليل الفني والبصري
st.markdown("### 📊 Engineering Optimization Plot")
col_chart, col_side = st.columns([3, 1])

with col_chart:
    fig = go.Figure()
    # IPR Curve
    fig.add_trace(go.Scatter(x=q_range, y=pwf_ipr, name="Reservoir IPR", 
                             line=dict(color='#3b82f6', width=4), fill='tozeroy'))
    # VLP Curve
    fig.add_trace(go.Scatter(x=q_range, y=pwf_vlp, name="Vertical Lift (VLP)", 
                             line=dict(color='#ef4444', width=4)))
    
    if opt_q > 0:
        fig.add_trace(go.Scatter(x=[opt_q], y=[opt_p], mode='markers', name="Optimal Point",
                                 marker=dict(size=18, color='#f59e0b', symbol='diamond', 
                                 line=dict(width=2, color='white'))))

    fig.update_layout(template="plotly_white", margin=dict(l=0, r=0, t=30, b=0), height=450,
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig, use_container_width=True)

with col_side:
    st.info("**Analysis Summary**")
    st.write(f"Well is performing at peak efficiency for a **{t_size}\"** tubing string.")
    if opt_p < 1000:
        st.warning("⚠️ Low FBHP: Risk of liquid loading detected.")
    else:
        st.success("✅ Stable flow conditions confirmed.")

st.markdown("---")
st.caption("Developed by Eng. Hussein Ali | Final Graduate Project Extension 2026")
