import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

st.set_page_config(page_title="🤖 AI Performance System", layout="wide")

st.markdown("""
    <style>
    .big-font {
        font-size:30px !important;
        color: #4CAF50;
    }
    .score-box {
        background-color: #1f1f2e;
        padding: 10px;
        border-radius: 15px;
        color: #fff;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 AI-Enabled Performance & Compensation System")
st.markdown("<p class='big-font'>For the Manufacturing Industry</p>", unsafe_allow_html=True)

st.markdown("### 📤 Upload Role-wise KPI Data (CSV)")
uploaded_file = st.file_uploader("Upload your file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File uploaded successfully!")
    
    st.subheader("📄 Raw Input Data")
    st.dataframe(df)

    # --- Performance Score Logic ---
    def compute_score(row):
        if row['Role'] == 'QC Inspector':
            return round((row['KPI1'] * 0.7 + row['KPI2'] / 250 * 0.3) * 100, 2)
        elif row['Role'] == 'Production Planner':
            return round((row['KPI1'] * 0.8 + row['KPI2'] / 10 * 0.2) * 100, 2)
        else:
            return np.nan

    df['Performance Score'] = df.apply(compute_score, axis=1)

    def compensation(score):
        if score >= 90:
            return "💰 ₹80,000 + 20% Bonus"
        elif score >= 80:
            return "🪙 ₹70,000 + 10% Bonus"
        elif score >= 70:
            return "💵 ₹60,000 + 5% Bonus"
        else:
            return "🧾 ₹50,000"

    df['Compensation'] = df['Performance Score'].apply(compensation)

    st.markdown("---")
    st.subheader("📊 Visual Performance Breakdown")

    # 📌 Average score per role
    avg_scores = df.groupby("Role")["Performance Score"].mean().reset_index()
    fig_bar = px.bar(avg_scores, x="Role", y="Performance Score", color="Role",
                     title="📈 Average Performance Score per Role", text_auto='.2s')
    st.plotly_chart(fig_bar, use_container_width=True)

    # 📌 Individual scores
    fig_scatter = px.scatter(df, x="KPI1", y="KPI2", color="Performance Score",
                             symbol="Role", size="Performance Score", hover_name="Name",
                             title="🎯 KPI Distribution and Score")
    st.plotly_chart(fig_scatter, use_container_width=True)

    # 📌 Show fancy cards
    st.markdown("### 🧠 AI Evaluation Summary")
    for index, row in df.iterrows():
        with st.container():
            st.markdown(f"""
            <div class='score-box'>
                <h4>{row['Name']} ({row['Role']})</h4>
                <b>Score:</b> {row['Performance Score']}<br>
                <b>Compensation:</b> {row['Compensation']}
            </div>
            """, unsafe_allow_html=True)
            time.sleep(0.05)

    # 📥 Download
    st.markdown("### 📥 Download AI Evaluation Report")
    st.download_button("Download CSV", df.to_csv(index=False), "evaluation_report.csv")

else:
    st.info("Upload a CSV with columns: Role, Name, KPI1, KPI2")
