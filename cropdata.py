import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np








# ---- USER LOGIN ----
def login():
    st.title("🔐 Crop Yield Dashboard Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":  # Change to your own credentials
            st.session_state["authenticated"] = True
            st.success("Logged in successfully")
        else:
            st.error("Incorrect username or password")


# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()  # Prevent the rest of the app from loading





# Load data
df = pd.read_excel("C:/Users/rival/OneDrive/Documents/2025 Documents/IIAFRICA/Capstone/Crop yield data sheet.xlsx")



# Title
st.title("🌾 Crop Yield Optimization Dashboard")

# Sidebar inputs
st.sidebar.header("🔍 Enter Environmental Conditions")
rain = st.sidebar.slider("Rainfall (mm)", 300, 1300, 800)
fert = st.sidebar.slider("Fertilizer", 40, 100, 70)
temp = st.sidebar.slider("Temperature (°C)", 20, 40, 30)
n = st.sidebar.slider("Nitrogen (N)", 60, 90, 75)
p = st.sidebar.slider("Phosphorus (P)", 15, 30, 20)
k = st.sidebar.slider("Potassium (K)", 15, 30, 20)

# --- Section 1: Data Overview ---
st.header("📊 Data Overview")
st.write("Sample of data:")
st.dataframe(df.head())

st.subheader("Correlation Heatmap")
fig, ax = plt.subplots()
sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="YlGnBu", ax=ax)
st.pyplot(fig)

# --- Section 2: Yield Predictor ---
st.header("🤖 Yield Predictor")

# Prepare features and model
X = df[["Rain Fall (mm)", "Fertilizer", "Temperatue", "Nitrogen (N)", "Phosphorus (P)", "Potassium (K)"]]
y = df["Yeild (Q/acre)"]
model = LinearRegression()
model.fit(X, y)

# Predict based on input
input_data = np.array([[rain, fert, temp, n, p, k]])
predicted_yield = model.predict(input_data)[0]
st.success(f"Estimated Yield: **{predicted_yield:.2f} Q/acre**")

# --- Section 3: Recommendations ---
st.header("📌 Recommendation")
if predicted_yield < 9:
    st.warning("⚠️ Yield is below average. Consider increasing Nitrogen or checking rainfall patterns.")
elif predicted_yield > 11:
    st.info("✅ Conditions are favorable for high yield.")
else:
    st.write("🟡 Moderate yield expected. You may fine-tune fertilizer or irrigation levels.")

if st.sidebar.button("Logout"):
    st.session_state["authenticated"] = False
    st.rerun()
