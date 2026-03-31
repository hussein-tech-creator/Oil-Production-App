import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="Petro-Optimizer Elite", layout="wide")
st.title("💎 Petro-Optimizer Elite: Nodal Analysis & Asset Valuation")
st.markdown("---")

# --- القائمة الجانبية المتقدمة ---
with st.sidebar:
    st.header("⚙️ Advanced Parameters")
    with st.expander("Reservoir (IPR)", expanded=True):
        p_res = st.number_input("Reservoir Pressure (psi)", value=3500)
        pi = st.slider("Productivity Index (J)", 0.1, 10.0, 1.5)
    
    with st.expander("Wellbore (VLP)", expanded=True):
        tubing_size = st.selectbox("Tubing Diameter (in)", [2.375, 2.875, 3.5, 4.5])
        p_whp = st.number_input("Wellhead Pressure (psi)", value=200)

    with st.expander("Economics & Market", expanded=True):
        oil_price = st.slider("Market Oil Price ($)", 40, 120, 85)
        lifting_cost = st.number_input("Lifting Cost ($/bbl)", value=15)

# --- 1. حسابات الـ Nodal Analysis (سر القيمة العالية) ---
q_range = np.linspace(0, p_res * pi, 50)
pwf_ipr = p_res - (q_range / pi)  # IPR Curve (Vogel-like linear simplification)

# VLP Curve (Simplified Physics-based model)
# كلما زاد التدفق، زاد فقد الضغط (Friction)، فاحتاج البئر لضغط أعلى للرفع
pwf_vlp = p_whp + (0.0005 * q_range**2 / (tubing_size/2.875)**4) + 1500 

# العثور على نقطة التقاطع (Operating Point)
idx = np.argwhere(np.diff(np.sign(pwf_ipr - pwf_vlp))).flatten()
opt_q = q_range[idx[0]] if len(idx) > 0 else 0
opt_p = pwf_ipr[idx[0]] if len(idx) > 0 else 0

# --- 2. عرض النتائج الاستراتيجية ---
st.subheader("📊 Optimization Dashboard")
m1, m2, m3 = st.columns(3)
m1.metric("Optimal Production Rate", f"{int(opt_q)} bbl/d", delta="Optimized")
m2.metric("Flowing BHP", f"{int(opt_p)} psi")
m3.metric("Daily Gross Profit", f"${int(opt_q * (oil_price - lifting_cost)):,}")

# --- 3. رسم منحنى الـ Nodal Analysis ---
fig_nodal = go.Figure()
fig_nodal.add_trace(go.Scatter(x=q_range, y=pwf_ipr, name="IPR (Reservoir)", line=dict(color='blue', width=3)))
fig_nodal.add_trace(go.Scatter(x=q_range, y=pwf_vlp, name="VLP (Wellbore)", line=dict(color='red', width=3)))

if opt_q > 0:
    fig_nodal.add_trace(go.Scatter(x=[opt_q], y=[opt_p], mode='markers+text', 
                                 name="Optimum Point", text=["MATCH"], 
                                 marker=dict(size=15, color='gold', symbol='star')))

fig_nodal.update_layout(title="Nodal Analysis: Reservoir vs Wellbore", 
                       xaxis_title="Flow Rate (bbl/d)", yaxis_title="Pressure (psi)")
st.plotly_chart(fig_nodal, use_container_width=True)

# --- 4. تحليل الحساسية (Sensitivity) ---
st.markdown("### 📈 Sensitivity: Impact of Tubing Size on Profit")
sizes = [2.375, 2.875, 3.5, 4.5]
profits = []
for s in sizes:
    temp_vlp = p_whp + (0.0005 * q_range**2 / (s/2.875)**4) + 1500
    temp_idx = np.argwhere(np.diff(np.sign(pwf_ipr - temp_vlp))).flatten()
    temp_q = q_range[temp_idx[0]] if len(temp_idx) > 0 else 0
    profits.append(temp_q * (oil_price - lifting_cost))

fig_sens = go.Figure(data=[go.Bar(x=[str(s) for s in sizes], y=profits, marker_color='teal')])
fig_sens.update_layout(title="Daily Profit by Tubing Size", yaxis_title="Profit ($/day)")
st.plotly_chart(fig_sens, use_container_width=True)

st.info("💡 Pro Tip: Increasing tubing size reduces friction but might cause liquid loading if rate is too low.")
