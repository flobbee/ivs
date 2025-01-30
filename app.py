# Import libraries
import streamlit as st
import numpy as np
import plotly.graph_objects as go
from IVS_call import implied_volatility as iv_call
from IVS_put import implied_volatility as iv_put

# Website Config
st.set_page_config(page_title="Implied Volatility Surface", page_icon="icon.png", layout="centered")

# Sidebar
st.sidebar.title("European Option")
option_type = st.sidebar.selectbox("Option Type", ["Call Option", "Put Option"])

st.sidebar.title("Parameters")
S = st.sidebar.number_input("Underlying/Spot Price ($)", min_value=1, value=100)
r = st.sidebar.number_input("Interest Rate (e.g. 0.05 for 5%)", min_value=0.0, value=0.05, format="%.4f")
if option_type == "Call Option":
    C = st.sidebar.number_input("Call Option Market Price ($)", min_value=0.01, value=10.0)
else:
    P = st.sidebar.number_input("Put Option Market Price ($)", min_value=0.01, value=10.0)

st.sidebar.title("Plot Ranges")
S_min = st.sidebar.number_input("Minimum Strike Price (% of Underlying Price)", min_value=0.10, value=0.80)
S_max = st.sidebar.number_input("Maximum Strike Price (% of Underlying Price)", min_value=1.10, value=1.20)
t_max = st.sidebar.number_input("Maximum Time to Expiration (Years)", min_value=0.2, value=1.0)

st.sidebar.subheader(" ")
st.sidebar.subheader("Created by Danny Zhou | [LinkedIn](www.linkedin.com/in/danny-zhou-b609942a4)")

# Define ranges for strike prices and expirations
X_values = np.linspace(S_min * S, S_max * S, 20)
T_values = np.linspace(0.1, t_max, 20)

# Compute implied volatilities
implied_vols = np.zeros((len(X_values), len(T_values)))
for i, X in enumerate(X_values):
    for j, t in enumerate(T_values):
        if option_type == "Call Option":
            implied_vols[i, j] = iv_call(C, S, X, t, r)
        else:
            implied_vols[i, j] = iv_put(P, S, X, t, r)

# Create 3D plot
X_mesh, T_mesh = np.meshgrid(T_values, X_values)
fig = go.Figure(data=[go.Surface(z=implied_vols, x=T_mesh, y=X_mesh, colorscale='viridis')])
fig.update_layout(
    title=f'Based on the Black-Scholes Model for {option_type}s',
    scene=dict(
        xaxis_title='Strike Price ($)',
        yaxis_title='Time to Expiration (Years)',
        zaxis_title='Implied Volatility',
        bgcolor='rgba(0,0,0,0)'
    ),
    template='plotly_dark',
    width=1500,
    height=800
)

# Display plot
st.title("Implied Volatility Surface")
st.plotly_chart(fig, use_container_width=True)
