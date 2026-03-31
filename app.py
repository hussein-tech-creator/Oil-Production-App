import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

# 1. إعدادات الصفحة (تصميم نظيف وعالي التباين)
st.set_page_config(page_title="Petro-Elite Dashboard", layout="wide", page_icon="🛢️")

st.markdown("""
    <style>
    /* خلفية بيضاء ساطعة لضمان الوضوح التام */
    .stApp { background-color: #ffffff; }
    
    /* تنسيق القائمة الجانبية بلون أزرق بترولي خفيف مريح للعين */
    section[data-testid="stSidebar"] {
        background-color: #f1f5f9;
        border-right: 2px solid #d1d9e6;
    }
    
    /* بطاقات النتائج Metrics بشكل بارز وأنيق */
    div[data-testid="stMetric"] {
        background-color: #f8fbff;
        border: 2px solid #e1e8f0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* تنسيق العناوين الاحترافي */
    h1, h2, h3, h4 { color: #003366; font-family: 'Arial', sans-serif; font-weight: 700; }
    
    /* حاوية لتوسيط الشعار وضبط حجمه */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. القائمة الجانبية بشعار (برج الحفر وقطرة النف
