# main.py
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Performance & Compensation", layout="centered")

st.title("📊 AI-Enabled Performance Management for Manufacturing")

uploaded_file = st.file_uploader("Upload Role-wise KPI Data (CSV)", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("### Input Data", df)

    def compute_score(row):
        if row['Role'] == 'QC Inspector':
            return round((row['KPI1'] * 0.7 + row['KPI2']/250 * 0.3) * 100, 2)
        elif row['Role'] == 'Production Planner':
            return round((row['KPI1'] * 0.8 + row['KPI2']/10 * 0.2) * 100, 2)
        else:
            return np.nan

    df['Performance Score'] = df.apply(compute_score, axis=1)

    # Tier-based compensation
    def compensation(score):
        if score >= 90:
            return "₹80,000 + 20% Bonus"
        elif score >= 80:
            return "₹70,000 + 10% Bonus"
        elif score >= 70:
            return "₹60,000 + 5% Bonus"
        else:
            return "₹50,000"

    df['Compensation Recommendation'] = df['Performance Score'].apply(compensation)

    st.write("### AI-Powered Evaluation")
    st.dataframe(df)

    st.download_button("Download Results as CSV", df.to_csv(index=False), "performance_results.csv")
