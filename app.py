import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# إعدادات الصفحة
st.set_page_config(page_title="Petro-Pro Analytics", layout="wide")

st.title("🛢️ Advanced Well Analytics & Forecasting")
st.markdown("---")

# --- القائمة الجانبية للمدخلات (Sidebar) ---
st.sidebar.header("Input Parameters")
q_i = st.sidebar.number_input("Initial Oil Rate (bbl/d)", value=1200)
d_i = st.sidebar.slider("Nominal Decline Rate (per year)", 0.1, 0.9, 0.3)
b = st.sidebar.slider("Decline Exponent (b-factor)", 0.0, 1.0, 0.5)
months = st.sidebar.slider("Forecast Period (Months)", 12, 120, 48)

# --- الحسابات الهندسية ---
time = np.arange(0, months + 1)
# معادلة Arps للنقصان
if b == 0: # Exponential
    q_t = q_i * np.exp(-d_i * time / 12)
else: # Hyperbolic
    q_t = q_i / (1 + b * (d_i / 12) * time)**(1/b)

# حساب الإنتاج التراكمي (EUR)
eur = np.trapz(q_t, time) * 30.44 # تحويل لبراميل تقريبية

# إنشاء الجدول
df = pd.DataFrame({
    "Month": time,
    "Oil Rate (bbl/d)": q_t.round(2),
    "Water Cut (%)": (20 + (time * 1.5)).clip(max=98) # مثال افتراضي لزيادة الماء
})

# --- عرض النتائج الرئيسية ---
col1, col2, col3 = st.columns(3)
col1.metric("Total Oil Recovery (EUR)", f"{int(eur):,} bbl")
col2.metric("Final Water Cut", f"{df['Water Cut (%)'].iloc[-1]} %")
col3.metric("Avg Oil Rate", f"{int(q_t.mean())} bbl/d")

# --- الرسم البياني ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=df["Month"], y=df["Oil Rate (bbl/d)"], name="Oil Rate", line=dict(color='green', width=3)))
fig.update_layout(title="Production Forecast", xaxis_title="Time (Months)", yaxis_title="Rate (bbl/d)")
st.plotly_chart(fig, use_container_width=True)

# --- المرحلة الأولى: أزرار التحميل الاحترافية ---
st.markdown("### 📥 Export & Reports")
col_down1, col_down2 = st.columns(2)

# تحويل البيانات لملف Excel في الذاكرة
output = BytesIO()
with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
    df.to_excel(writer, index=False, sheet_name='Forecast')
processed_data = output.getvalue()

with col_down1:
    st.download_button(
        label="Download Data as Excel",
        data=processed_data,
        file_name='well_forecast_report.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

with col_down2:
    st.download_button(
        label="Download Data as CSV",
        data=df.to_csv(index=False).encode('utf-8'),
        file_name='well_forecast_data.csv',
        mime='text/csv'
    )

st.info("Tip: Use these files to attach in your weekly production meeting reports.")
