import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Tourism Dashboard", layout="wide")

st.title("🌍 Tourism Analytics Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("final_dataset.csv")
    return df

df = load_data()

# -----------------------------
# SIDEBAR FILTERS (AUTO-ADJUSTING)
# -----------------------------
st.sidebar.header("User Input")

# Year filter
year = st.sidebar.selectbox(
    "Visit Year",
    sorted(df["VisitYear"].unique())
)

df_year = df[df["VisitYear"] == year]

# Month filter (based on year)
month = st.sidebar.selectbox(
    "Visit Month",
    sorted(df_year["VisitMonth"].unique())
)

df_month = df_year[df_year["VisitMonth"] == month]

# City filter (based on year + month)
city = st.sidebar.selectbox(
    "City",
    sorted(df_month["CityId"].unique())
)

df_city = df_month[df_month["CityId"] == city]

# Attraction Type filter (based on all above)
atype = st.sidebar.selectbox(
    "Attraction Type",
    sorted(df_city["AttractionType"].unique())
)

filtered_df = df_city[df_city["AttractionType"] == atype]

# -----------------------------
# DATA PREVIEW
# -----------------------------
st.subheader("Dataset Preview (Full Data)")
st.dataframe(df.head(10))

st.subheader("Filtered Data")

if filtered_df.empty:
    st.warning("No data found (this should not happen now)")
else:
    st.dataframe(filtered_df.head(10))

# -----------------------------
# KEY METRICS
# -----------------------------
st.subheader("Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Visits", len(filtered_df))
col2.metric("Average Rating", round(filtered_df["Rating"].mean(), 2))
col3.metric("Unique Attractions", filtered_df["AttractionId"].nunique())

# -----------------------------
# TOP RECOMMENDATIONS
# -----------------------------
st.subheader("Top Recommendations")

top = (
    filtered_df.groupby("AttractionId")["Rating"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
    .reset_index()
)

st.dataframe(top)

# -----------------------------
# CHARTS (MATPLOTLIB - NO ERRORS)
# -----------------------------
st.subheader("Data Insights")

col1, col2 = st.columns(2)

# Visit Mode Chart
with col1:
    st.write("Visit Mode Distribution")
    fig1, ax1 = plt.subplots()
    filtered_df["VisitMode"].value_counts().plot(kind='bar', ax=ax1)
    st.pyplot(fig1)

# Rating Distribution
with col2:
    st.write("Rating Distribution")
    fig2, ax2 = plt.subplots()
    filtered_df["Rating"].plot(kind='hist', bins=5, ax=ax2)
    st.pyplot(fig2)

# -----------------------------
# KEY INSIGHTS
# -----------------------------
st.subheader("Key Insights")

if not filtered_df.empty:
    st.write("Most Common Visit Mode:", filtered_df["VisitMode"].mode()[0])
    st.write("Most Popular Attraction Type:", filtered_df["AttractionType"].mode()[0])
    st.write("Highest Rated Attraction:", top.iloc[0]["AttractionId"])