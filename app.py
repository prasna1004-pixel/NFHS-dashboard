import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="NFHS Change Dashboard",
    layout="wide"
)

# Title
st.title("📊 NFHS-4 vs NFHS-5 Health Indicators Dashboard")
st.caption("District & State-wise Change Analysis | India")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("India_Change.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")

state = st.sidebar.selectbox(
    "Select State",
    sorted(df["State"].unique())
)

districts = df[df["State"] == state]["District Name"].unique()
district = st.sidebar.selectbox(
    "Select District",
    sorted(districts)
)

category = st.sidebar.selectbox(
    "Select Category",
    sorted(df["Category"].unique())
)

# Filtered Data
filtered_df = df[
    (df["State"] == state) &
    (df["District Name"] == district) &
    (df["Category"] == category)
]

# KPI Metrics
st.subheader(f"📍 {district}, {state}")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Average NFHS-4",
    round(filtered_df["NFHS 4"].mean(), 2)
)

col2.metric(
    "Average NFHS-5",
    round(filtered_df["NFHS 5"].mean(), 2)
)

col3.metric(
    "Average Change",
    round(filtered_df["Change"].mean(), 2)
)

st.divider()

# Bar Chart – NFHS 4 vs 5
st.subheader("📈 Indicator Comparison")

fig = px.bar(
    filtered_df,
    x="Indicator",
    y=["NFHS 4", "NFHS 5"],
    barmode="group",
    title="NFHS-4 vs NFHS-5 Comparison",
    labels={"value": "Percentage", "variable": "Survey"}
)

st.plotly_chart(fig, use_container_width=True)

# Change Analysis
st.subheader("📉 Change in Indicators")

fig2 = px.bar(
    filtered_df,
    x="Indicator",
    y="Change",
    title="Change Between NFHS-4 and NFHS-5",
    color="Change"
)

st.plotly_chart(fig2, use_container_width=True)

# Data Table
st.subheader("📋 Detailed Data")
st.dataframe(filtered_df)

# Footer
st.caption("Source: National Family Health Survey (NFHS-4 & NFHS-5)")
