import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

from styles import load_css
from utils import (
    prepare_input,
    predict_price,
    vehicle_health,
    vehicle_condition,
    depreciation,
    summary,
    health_color
)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Used Car Price Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_css()

# ==========================================
# LOAD FILES
# ==========================================

@st.cache_resource
def load_model():
    return joblib.load("used_car_price_model.pkl")

@st.cache_data
def load_dataset():
    return pd.read_csv("car_data.csv")

@st.cache_data
def load_features():
    return joblib.load("feature_columns.pkl")

model = load_model()
df = load_dataset()
feature_columns = load_features()

# ==========================================
# SESSION STATE
# ==========================================

if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "history" not in st.session_state:
    st.session_state.history = []

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/741/741407.png",
        width=120
    )

    st.title("🚗 Car Price Predictor")

    st.markdown("---")

    st.success("Machine Learning Project")

    st.metric(
        "Model",
        "Random Forest"
    )

    st.metric(
        "Accuracy",
        "93.9%"
    )

    st.metric(
        "Dataset",
        f"{len(df):,}"
    )

    st.metric(
        "Brands",
        df["brand"].nunique()
    )

    st.markdown("---")

    st.info(
        """
Python

Scikit-Learn

Streamlit

Pandas

Plotly
"""
    )

# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="main-title">
🚗 Used Car Price Prediction Dashboard
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="sub-title">
Predict the resale value of your used vehicle using Machine Learning.
</div>
""", unsafe_allow_html=True)

st.write("")

# ==========================================
# KPI CARDS
# ==========================================

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
<div class="metric-card">
<h3>Cars</h3>
<h1>{len(df):,}</h1>
</div>
""", unsafe_allow_html=True)

with k2:
    st.markdown("""
<div class="metric-card">
<h3>Accuracy</h3>
<h1>93.9%</h1>
</div>
""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
<div class="metric-card">
<h3>Brands</h3>
<h1>{df["brand"].nunique()}</h1>
</div>
""", unsafe_allow_html=True)

with k4:
    st.markdown("""
<div class="metric-card">
<h3>Algorithm</h3>
<h1>Random Forest</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# INPUT SECTION
# ==========================================

st.subheader("🚘 Enter Vehicle Details")

left, right = st.columns(2)

with left:

    brand = st.selectbox(
        "Brand",
        sorted(df["brand"].dropna().unique())
    )

    model_name = st.selectbox(
        "Model",
        sorted(
            df[df["brand"] == brand]["model"]
            .dropna()
            .unique()
        )
    )

    vehicle_age = st.slider(
        "Vehicle Age (Years)",
        0,
        20,
        5
    )

    km_driven = st.number_input(
        "Kilometers Driven",
        min_value=0,
        value=50000,
        step=1000
    )

    mileage = st.number_input(
        "Mileage (km/l)",
        min_value=0.0,
        value=18.0,
        step=0.1
    )

with right:

    engine = st.number_input(
        "Engine (CC)",
        min_value=500,
        value=1200
    )

    max_power = st.number_input(
        "Max Power (bhp)",
        min_value=20,
        value=100
    )

    seats = st.selectbox(
        "Seats",
        sorted(df["seats"].dropna().unique())
    )

    fuel_type = st.selectbox(
        "Fuel Type",
        sorted(df["fuel_type"].dropna().unique())
    )

    transmission_type = st.selectbox(
        "Transmission",
        sorted(df["transmission_type"].dropna().unique())
    )

    seller_type = st.selectbox(
        "Seller Type",
        sorted(df["seller_type"].dropna().unique())
    )

st.write("")

# ==========================================
# BUTTONS
# ==========================================

b1, b2 = st.columns([4,1])

with b1:

    predict_btn = st.button(
        "🚀 Predict Price",
        use_container_width=True
    )

with b2:

    if st.button(
        "🔄 Reset",
        use_container_width=True
    ):

        st.session_state.prediction = None
        st.session_state.history = []

        st.rerun()

st.markdown("---")

# ==========================================
# PREDICTION ENGINE
# ==========================================

if predict_btn:

    input_data = prepare_input(
        feature_columns=feature_columns,
        vehicle_age=vehicle_age,
        km_driven=km_driven,
        mileage=mileage,
        engine=engine,
        max_power=max_power,
        seats=seats,
        brand=brand,
        model_name=model_name,
        fuel_type=fuel_type,
        seller_type=seller_type,
        transmission_type=transmission_type
    )

    prediction = predict_price(
        model,
        input_data
    )

    st.session_state.prediction = prediction

    st.session_state.history.append({
        "Brand": brand,
        "Model": model_name,
        "Price": prediction
    })

# ==========================================
# RESULT SECTION
# ==========================================

if st.session_state.prediction is not None:

    prediction = st.session_state.prediction

    health_score = vehicle_health(
        vehicle_age,
        km_driven,
        mileage
    )

    condition, color = vehicle_condition(
        health_score
    )

    info = summary(
        prediction,
        health_score
    )

    # ==========================
    # BIG PRICE CARD
    # ==========================

    st.markdown(f"""
    <div class="price-card">

    <h2>💰 Estimated Car Price</h2>

    <h1>
    ₹ {prediction:,.0f}
    </h1>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    # ==========================
    # KPI ROW
    # ==========================

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Vehicle Health",
            f"{health_score}/100"
        )

    with c2:

        st.metric(
            "Condition",
            condition
        )

    with c3:

        st.metric(
            "Category",
            info["category"]
        )

    st.write("")

    # ==========================
    # HEALTH BAR
    # ==========================

    st.subheader("❤️ Vehicle Health Score")

    st.progress(int(health_score))

    st.success(
        f"Vehicle Health : {health_score}/100"
    )

    # ==========================
    # CONDITION MESSAGE
    # ==========================

    if health_score >= 85:

        st.success(
            "Excellent Condition Vehicle"
        )

    elif health_score >= 70:

        st.success(
            "Good Condition Vehicle"
        )

    elif health_score >= 50:

        st.warning(
            "Fair Condition Vehicle"
        )

    else:

        st.error(
            "Poor Condition Vehicle"
        )

    st.markdown("---")
    
    # ==========================================
# DEPRECIATION FORECAST
# ==========================================

if st.session_state.prediction is not None:

    st.subheader("📉 Estimated Depreciation")

    dep = depreciation(st.session_state.prediction)

    dep_df = pd.DataFrame({
        "Year": list(dep.keys()),
        "Estimated Price": list(dep.values())
    })

    fig = px.line(
        dep_df,
        x="Year",
        y="Estimated Price",
        markers=True,
        title="Expected Vehicle Value Over Time"
    )

    fig.update_layout(
        template="plotly_dark",
        height=420
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# DATASET ANALYTICS
# ==========================================

st.markdown("---")

st.subheader("📊 Dataset Analytics")

col1, col2 = st.columns(2)

with col1:

    brand_chart = (
        df["brand"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    brand_chart.columns = [
        "Brand",
        "Cars"
    ]

    fig = px.bar(
        brand_chart,
        x="Brand",
        y="Cars",
        color="Cars",
        title="Top 10 Brands"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with col2:

    fuel_chart = (
        df["fuel_type"]
        .value_counts()
        .reset_index()
    )

    fuel_chart.columns = [
        "Fuel",
        "Count"
    ]

    fig = px.pie(
        fuel_chart,
        names="Fuel",
        values="Count",
        hole=.5,
        title="Fuel Distribution"
    )

    fig.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ==========================================
# PREDICTION HISTORY
# ==========================================

if len(st.session_state.history) > 0:

    st.markdown("---")

    st.subheader("🕒 Prediction History")

    history_df = pd.DataFrame(
        st.session_state.history
    )

    history_df["Price"] = history_df[
        "Price"
    ].apply(
        lambda x: f"₹ {x:,.0f}"
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

# ==========================================
# QUICK DATA INSIGHTS
# ==========================================

st.markdown("---")

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Average Selling Price",
        f"₹ {df['selling_price'].mean():,.0f}"
    )

with c2:

    st.metric(
        "Average Vehicle Age",
        f"{df['vehicle_age'].mean():.1f} Years"
    )

with c3:

    st.metric(
        "Average KM Driven",
        f"{df['km_driven'].mean():,.0f}"
    )

# ==========================================
# DOWNLOAD REPORT
# ==========================================

if st.session_state.prediction is not None:

    report = pd.DataFrame({

        "Brand":[brand],

        "Model":[model_name],

        "Predicted Price":[
            st.session_state.prediction
        ],

        "Fuel":[fuel_type],

        "Transmission":[transmission_type],

        "Health Score":[health_score],

        "Condition":[condition]

    })

    csv = report.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "📥 Download Prediction Report",

        csv,

        "prediction_report.csv",

        "text/csv"

    )

# ==========================================
# FOOTER
# ==========================================

st.markdown("---")

st.markdown("""

<div class="footer">

🚗 Used Car Price Prediction System

Built using

Python • Scikit-Learn • Streamlit • Plotly

Random Forest Regressor

© 2026 Rahul Mishra

</div>

""", unsafe_allow_html=True)