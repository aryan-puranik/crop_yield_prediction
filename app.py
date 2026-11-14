"""
Crop Yield Prediction & Forecasting - Streamlit Application
Author: Aryan Puranik
Academic Research Project: Crop Yield Prediction and Forecasting Using Agricultural Data and Machine Learning
"""

import sys
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Crop Yield Prediction System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load model pipeline
@st.cache_resource
def load_model():
    model_path = Path(__file__).resolve().parent / "models" / "best_pipeline.joblib"
    if not model_path.exists():
        st.error(f"Trained model not found at {model_path}. Please run notebook 04 first.")
        st.stop()
    return joblib.load(model_path)

pipeline = load_model()

# Categorical options
CROPS = [
    "Barley", "Castor", "Chickpea", "Cotton", "Finger Millet", "Groundnut", 
    "Linseed", "Maize", "Minor Pulses", "Pearl Millet", "Pigeonpea", 
    "Rapeseed & Mustard", "Rice", "Safflower", "Sesamum", "Sorghum (Kharif)", 
    "Sorghum (Rabi)", "Soybean", "Sugarcane", "Sunflower", "Wheat"
]

SOIL_TYPES = [
    "Alfisols", "Aridisols", "Entisols", "Inceptisols", "Mollisols", "Vertisols"
]

# Historical benchmark medians (kg/ha) from exploratory data analysis
CROP_MEDIANS = {
    "Sugarcane": 5200.0, "Wheat": 2840.0, "Rice": 2410.0, "Barley": 2440.0,
    "Maize": 1980.0, "Groundnut": 1500.0, "Pearl Millet": 1310.0, "Finger Millet": 1250.0,
    "Sorghum (Kharif)": 1150.0, "Sorghum (Rabi)": 1090.0, "Soybean": 980.0,
    "Chickpea": 675.0, "Rapeseed & Mustard": 850.0, "Pigeonpea": 720.0,
    "Castor": 850.0, "Linseed": 450.0, "Sunflower": 580.0, "Sesamum": 380.0,
    "Minor Pulses": 420.0, "Safflower": 520.0, "Cotton": 212.0
}

# App header
st.title("🌾 Crop Yield Prediction & Forecasting System")
st.markdown("""
**Author:** Aryan Puranik &nbsp;|&nbsp; **Model:** Extra Trees Regressor &nbsp;|&nbsp; **Historical Scope:** 1966–2017  
Predict expected agricultural crop yield (kg/ha) based on district geography, soil taxonomy, climate parameters, and macronutrient applications.
""")
st.divider()

# Sidebar for metadata & info
with st.sidebar:
    st.header("ℹ️ Project Information")
    st.markdown("""
    This application deploys a scikit-learn machine learning pipeline trained on 46 years of district-level Indian agricultural data.
    
    **Pipeline Architecture:**
    - Standard Scaling on continuous climate and soil nutrients.
    - One-Hot Encoding for categorical features.
    - Extra Trees ensemble regressor.
    
    **Evaluation Protocol:**
    - Chronological evaluation on unseen 2015–2017 seasons.
    - Test $R^2$: **0.72** | Test MAE: **520.8 kg/ha**.
    """)
    st.info("💡 **Viva Defense Tip:** Yield (kg/ha) measures agricultural productivity per unit area, avoiding acreage confounding associated with total production.")

# Main Form
col_geo, col_clim, col_soil = st.columns(3)

with col_geo:
    st.subheader("📍 Location & Crop")
    selected_crop = st.selectbox("Crop Type", CROPS, index=CROPS.index("Wheat"))
    selected_region = st.text_input("District / State", value="Ludhiana, Punjab", help="Format: District, State")
    selected_soil = st.selectbox("Soil Taxonomy", SOIL_TYPES, index=SOIL_TYPES.index("Inceptisols"))
    target_year = st.number_input("Target Year", min_value=2018, max_value=2035, value=2024, step=1)

with col_clim:
    st.subheader("🌦️ Climate Conditions")
    temperature = st.slider("Mean Temperature (°C)", min_value=5.0, max_value=45.0, value=24.5, step=0.1)
    rainfall = st.slider("Annual / Seasonal Rainfall (mm)", min_value=50.0, max_value=3500.0, value=750.0, step=10.0)
    humidity = st.slider("Relative Humidity (%)", min_value=15.0, max_value=100.0, value=65.0, step=1.0)
    pesticide = st.number_input("Pesticide Application (kg/ha)", min_value=0.01, max_value=5.0, value=0.35, step=0.05)

with col_soil:
    st.subheader("🧪 Soil Nutrients & pH")
    ph = st.slider("Soil pH", min_value=4.0, max_value=9.5, value=7.2, step=0.1)
    nitrogen = st.number_input("Nitrogen (N) (kg/ha)", min_value=0.0, max_value=300.0, value=85.0, step=5.0)
    phosphorus = st.number_input("Phosphorus (P) (kg/ha)", min_value=0.0, max_value=200.0, value=40.0, step=5.0)
    potassium = st.number_input("Potassium (K) (kg/ha)", min_value=0.0, max_value=200.0, value=35.0, step=5.0)

st.divider()

# Predict Button
predict_btn = st.button("🚀 Predict Crop Yield", type="primary", use_container_width=True)

if predict_btn:
    input_data = pd.DataFrame([{
        "Region": selected_region,
        "Crop": selected_crop,
        "Soil Type": selected_soil,
        "Year": target_year,
        "Temperature": temperature,
        "Rainfall": rainfall,
        "Humidity": humidity,
        "pH": ph,
        "Nitrogen": nitrogen,
        "Phosphorus": phosphorus,
        "Potassium": potassium,
        "Pesticide": pesticide
    }])
    
    with st.spinner("Calculating forecast..."):
        try:
            pred_yield = float(pipeline.predict(input_data)[0])
            pred_yield = max(0.0, pred_yield)
            
            # Unit conversions
            yield_tonnes_ha = pred_yield / 1000.0
            yield_quintals_acre = pred_yield / 247.1
            hist_median = CROP_MEDIANS.get(selected_crop, 1500.0)
            diff_pct = ((pred_yield - hist_median) / hist_median) * 100
            
            st.success("✅ Prediction Successfully Generated!")
            
            # Metric cards
            res_col1, res_col2, res_col3, res_col4 = st.columns(4)
            with res_col1:
                st.metric("Predicted Yield", f"{pred_yield:,.1f} kg/ha")
            with res_col2:
                st.metric("In Tonnes / Hectare", f"{yield_tonnes_ha:.2f} t/ha")
            with res_col3:
                st.metric("In Quintals / Acre", f"{yield_quintals_acre:.1f} q/acre")
            with res_col4:
                st.metric("Vs Historical Median", f"{pred_yield - hist_median:+,.1f} kg/ha", delta=f"{diff_pct:+.1f}%")
                
            # Domain Context Callout
            st.info(f"🌾 **Crop Context for {selected_crop}:** Historical median yield in the national dataset is **{hist_median:,.0f} kg/ha**. "
                    f"Your predicted yield of **{pred_yield:,.1f} kg/ha** reflects local weather, soil, and management inputs.")
            
        except Exception as e:
            st.error(f"Error generating prediction: {str(e)}")

st.divider()
st.caption("Academic Machine Learning Project • Built with Python, Scikit-Learn, and Streamlit • Authored by Aryan Puranik")
