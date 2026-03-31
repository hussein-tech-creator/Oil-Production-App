import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# إعدادات الصفحة
st.set_page_config(page_title="Petro-Economics Pro", layout="wide")

st.title("🛢️ Advanced Well Analytics & Economics")
st.markdown("---")

# --- القائمة الجانبية (Sidebar) ---
st.sidebar.header("1. Engineering Parameters")
q_i = st.sidebar.number_input("Initial Oil Rate (bbl/d)", value=1200)
d_i = st.sidebar.slider("Decline Rate (per year)", 0.1, 0.9, 0.3)
b = st.sidebar.slider("Decline Exponent (b-factor)", 0.0, 1.0, 0.5)
months = st.sidebar.slider("Forecast Period (Months)", 12, 120, 60)

st.sidebar.header("2. Economic Parameters")
oil_price = st.sidebar.slider("Oil Price ($/bbl)", 40, 150, 85)
opex = st.sidebar.number_input("Operating Cost ($/bbl)", value=25)

# --- الحسابات الهندسية والمالية ---
time = np.arange(0, months + 1)
if b == 0:
    q_t = q_i * np.exp(-d_i * time / 12)
else:
    q_t = q_i / (1 + b * (d_i / 12) * time)**(1/b)

eur = np.trapz(q_t, time) * 30.44
net_profit_per_bbl = oil_price - opex
total_revenue = eur * net_profit_per_bbl

# حساب الحد الاقتصادي (Economic Limit)
# نفترض أن البئر يتوقف اقتصادياً إذا أصبح معدل الإنتاج لا يغطي تكلفة التشغيل الثابتة (مثال تبسيطي)
economic_limit_rate = 50 # برميل في اليوم كحد أدنى افتراضي

# إنشاء الجدول
df = pd.DataFrame({
    "Month": time,
    "Oil Rate (bbl/d)": q_t.round(2),
    "Monthly Revenue ($)": (q_t * 30.44 * net_profit_per_bbl).round(0)
})

# --- عرض النتائج الرئيسية ---
col1, col2, col3 = st.columns(3)
col1.metric("Estimated EUR", f"{int(eur):,} bbl")
col2.metric("Projected Net Revenue", f"${int(total_revenue):,}")
col3.metric("Profit per Barrel", f"${net_profit_per_bbl}")

# --- الرسم البياني المطور ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Month"], y=df["Oil Rate (bbl/d)"], name="Production Forecast", line=dict(color='#2ecc71', width=3)))
# إضافة خط الحد الاقتصادي
fig.add_hline(y=economic_limit_rate, line_dash="dot", line_color="red", annotation_text="Economic Limit")

fig.update_layout(title="Production & Economic Forecast", xaxis_title="Months", yaxis_title="Rate (bbl/d)")
st.plotly_chart(fig, use_container_width=True)

# --- التنبيهات الذكية ---
if q_t[-1] < economic_limit_rate:
    st.warning(f"⚠️ Warning: Well reaches economic limit before month {months}. Consider Workover or Plug & Abandonment.")
else:
    st.success("✅ Well remains profitable throughout the forecast period.")

# --- أزرار التحميل ---
st.markdown("### 📥 Download Professional Reports")
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Economics')
processed_data = output.getvalue()

st.download_button(label="Download Economic Report (Excel)", data=processed_data, file_name='well_economics_report.xlsx')
