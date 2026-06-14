import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Show the lockout screen if not authorized
if not st.session_state["authenticated"]:
    # Red system title matching your warning theme
    st.markdown("<h1 style='color: #ffffff; text-align: center;'>Youve been stopped by JD vance</h1>", unsafe_allow_html=True)
    
    # Optional sub-warning description
    st.markdown("<p style='text-align: center; color: #ffffff;'>Reason:Suspected Antisemite.</p>", unsafe_allow_html=True)
    
    # Displays your warning image (Swap URL with your preferred graphic if desired)
    st.image(
        "https://i.imgflip.com/a2jkgz.png", 
        caption="ECT SECURITY SYSTEM GATEWAY",
        use_container_width=True
    )
    
    st.markdown("---")
    
    # Protected password text input field 
    user_code = st.text_input("", type="password")
    
    # Change "YOUR_SECRET_CODE" to your chosen password string
    if user_code == "weloveisreal":
        st.session_state["authenticated"] = True
        st.rerun()
    elif user_code != "":
        st.error("ACCESS DENIED: JEW")
        
    st.stop()
        
    st.stop()
def style_plot(fig):
    fig.update_layout(
        paper_bgcolor="#1C2530",
        plot_bgcolor="#1C2530",
        font=dict(color="white"),
        title_font=dict(color="#1b5fab", size=18),
        legend_font=dict(color="white"),
        xaxis=dict(gridcolor="#2F4257", zerolinecolor="#2F4257"),
        yaxis=dict(gridcolor="#2F4257", zerolinecolor="#2F4257")
    )
    return fig

# ==========================================
# PAGE CONFIG & THEME
# ==========================================
st.set_page_config(
    page_title="JSP ICBM Simulation",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* FORCE BUILT-IN SYSTEM MONOSPACE FONTS GLOBALLY */
html, body, .stApp, [data-testid="stMain"], [data-testid="stSidebar"], * {
    font-family: 'Orbitron', 'Orbitron-Bold', sans-serif !important;
}

/* YOUR EXACT COLORS & STYLES (COMPLETELY UNTOUCHED) */
.stApp {
    background-image: url("https://www.transparenttextures.com/patterns/asfalt-dark.png");
    background-repeat: repeat;
    background-attachment: fixed;
    background-color: #525559;
}

[data-testid="stSidebar"] { background-color: #18202B; }

section[data-testid="stSidebar"] div[data-baseweb="input"] input {
    background-color: #525559 !important;
    color: #e9f7ea !important;
    border: 1px solid #2F4257 !important;
}

section[data-testid="stSidebar"] textarea {
    background-color: #525559 !important;
    color: #219ebc !important;
    border: 1px solid #2F4257 !important;
}

section[data-testid="stSidebar"] label { color: #219ebc !important; }
p, div, label, span { color: #c9d0d9 !important; }
h1 { color: #861211 !important; font-size: 3rem !important; }
h2, h3 { color: #1b5fab !important; }

[data-testid="metric-container"] {
    background-color: #1C2530;
    border: 1px solid #2F4257;
    border-radius: 15px;
    padding: 15px;
}

[data-testid="stMetricValue"] { color: #1b5fab !important; font-size: 2rem !important; }
[data-testid="stMetricLabel"] { color: #FFFFFF !important; }
.streamlit-expanderHeader { color: white !important; }

div[data-testid="stPlotlyChart"] {
    border-radius: 20px !important;
    overflow: hidden !important;
    border: 1px solid #2F4257;
}
</style>
""", unsafe_allow_html=True)

st.title("JSP ICBM Simulation")
st.markdown("### Highly inacurate-extremely slow")
st.markdown("---")

# ==========================================
# 1. SIDEBAR PANEL
# ==========================================
st.sidebar.header("Rocket Configuration")
empty_mass = st.sidebar.number_input("Empty Mass (kg)", min_value=0.0001, max_value=10.0, value=0.3766, step=0.0001, format="%.4f")
fuel_mass = st.sidebar.number_input("Initial Fuel Mass (kg)", min_value=0.0, max_value=5.0, value=0.16, step=0.0001, format="%.4f")
frontal_area = st.sidebar.number_input("Frontal Area (m²)", min_value=0.0001, max_value=0.1, value=0.0014998, format="%.7f")
drag_coeff = st.sidebar.number_input("Drag Coefficient (CD)", min_value=0.0, max_value=2.0, value=0.55, step=0.01)
launch_alt = st.sidebar.number_input("Launch Altitude (m absl)", min_value=0.0, max_value=10000.0, value=200.0, step=10.0)

st.sidebar.markdown("---")
st.sidebar.header("Thrust Curve Data")
st.sidebar.markdown("50samples per second pls")
default_thrust = "80\n100\n120\n140\n160\n180\n182\n184\n186\n188\n190\n192\n194\n196\n198\n200\n200\n200\n200\n200\n200\n198\n196\n194\n192\n190\n188\n186\n184\n182\n180\n179\n178\n177\n176\n175\n168\n161\n154\n147\n140\n124\n100\n92\n76\n60\n52\n44\n36\n28\n20"
thrust_input = st.sidebar.text_area("Thrust Profile (N)", value=default_thrust, height=180)

thrust_curve = [float(line.strip()) for line in thrust_input.split("\n") if line.strip()]

st.sidebar.markdown("---")
st.sidebar.header("Actual Flight Telemetry")
st.sidebar.markdown("10samples per second pls (0.1s steps)")
default_baro = "0\n5\n18\n38\n65\n98\n135\n175\n218\n262\n305\n348\n388\n425\n458\n488\n513\n534\n550\n561\n567\n569\n566\n559\n548\n533\n514"
baro_input = st.sidebar.text_area("Barometer Altitude (m)", value=default_baro, height=180)

baro_curve = [float(line.strip()) for line in baro_input.split("\n") if line.strip()]

# ========================================== 
# 2. RUN SIMULATION PHYSICS
# ==========================================
dt = 0.02  
max_steps = 2500  
g0 = 9.81  

time_history, mass_history, thrust_history, fg_history = [], [], [], []
fnet_history, accel_history, vel_history = [], [], []
alt_gain_history, alt_absl_history, drag_history, fuel_mass_history = [], [], [], []

velocity = 0.0
alt_gain = 0.0
alt_absl = launch_alt
current_fuel = fuel_mass
burn_steps = len(thrust_curve)
fuel_per_step = (fuel_mass / burn_steps) if burn_steps > 0 else 0

for step in range(max_steps):
    t = round((step + 1) * dt, 2)
    thrust = thrust_curve[step] if step < burn_steps else 0.0
    current_fuel = max(0.0, fuel_mass - (step * fuel_per_step)) if step < burn_steps else 0.0
    total_mass = empty_mass + current_fuel
    
    air_density = 1.225 * np.exp(-alt_absl / 8500.0)
    drag_force = 0.5 * air_density * (velocity ** 2) * drag_coeff * frontal_area
    if velocity < 0:
        drag_force = -drag_force
        
    gravity_force = total_mass * g0
    net_force = thrust - gravity_force - drag_force if velocity >= 0 else thrust - gravity_force + drag_force
    acceleration = net_force / total_mass
    
    velocity += acceleration * dt
    alt_gain += velocity * dt
    alt_absl = launch_alt + alt_gain
    
    if alt_absl < 0 and step > burn_steps:
        break
        
    time_history.append(t)
    mass_history.append(total_mass)
    thrust_history.append(thrust)
    fg_history.append(gravity_force)
    fnet_history.append(net_force)
    accel_history.append(acceleration)
    vel_history.append(velocity)
    alt_gain_history.append(alt_gain)
    alt_absl_history.append(alt_absl)
    drag_history.append(drag_force)
    fuel_mass_history.append(current_fuel)

sim_df = pd.DataFrame({
    "Time (s)": time_history,
    "Total Mass (kg)": mass_history,
    "Fuel Mass (kg)": fuel_mass_history,
    "Thrust (N)": thrust_history,
    "Net Force (N)": fnet_history,
    "Drag Force (N)": drag_history,
    "Acceleration (m/s²)": accel_history,
    "Velocity (m/s)": vel_history,
    "Altitude Gain (m)": alt_gain_history,
    "Absolute Altitude (m)": alt_absl_history
})

# Clean merge engine for 0.1s step barometer telemetry data
if baro_curve:
    baro_times = [round((i + 1) * 0.1, 2) for i in range(len(baro_curve))]
    baro_df = pd.DataFrame({"Time (s)": baro_times, "Actual Altitude (m)": baro_curve})
    sim_df = pd.merge_asof(sim_df, baro_df, on="Time (s)", direction="nearest", tolerance=0.05)

# ==========================================
# 3. MISSION METRICS
# ==========================================
max_alt = sim_df["Altitude Gain (m)"].max() if not sim_df.empty else launch_alt
max_vel = sim_df["Velocity (m/s)"].max() if not sim_df.empty else 0.0
max_g = ((sim_df["Acceleration (m/s²)"].max() / 9.81) + 1) if not sim_df.empty else 1.0

st.subheader("[china] Mission Summary")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label="Apogee", value=f"{max_alt:,.1f} m")
with col2:
    st.metric(label="Maximum Velocity", value=f"{max_vel:,.1f} m/s", delta=f"{max_vel*3.6:,.0f} km/h")
with col3:
    st.metric(label="Peak G-Load", value=f"{max_g:.2f} G")
st.markdown("---")

# ==========================================
# 4. CHARTS
# ==========================================
st.subheader("Flight Simulation Profiles")

row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    altitude_cols = ["Altitude Gain (m)"]
    if "Actual Altitude (m)" in sim_df.columns:
        altitude_cols.append("Actual Altitude (m)")
        
    fig_alt = px.line(sim_df, x="Time (s)", y=altitude_cols, title="Altitude Profile over Time", template="plotly_dark")
    fig_alt.update_traces(line_color="#00FFCC", selector=dict(name="Altitude Gain (m)"))
    if "Actual Altitude (m)" in sim_df.columns:
        fig_alt.update_traces(line=dict(color="#FFCC00", dash="dash"), selector=dict(name="Actual Altitude (m)"))
    st.plotly_chart(style_plot(fig_alt), use_container_width=True)

with row1_col2:
    fig_vel = px.line(sim_df, x="Time (s)", y="Velocity (m/s)", title="Velocity Profile over Time", template="plotly_dark")
    fig_vel.update_traces(line_color="#FF3366")
    st.plotly_chart(style_plot(fig_vel), use_container_width=True)

row2_col1, row2_col2 = st.columns(2)
with row2_col1:
    fig_forces = px.line(sim_df, x="Time (s)", y=["Thrust (N)", "Drag Force (N)", "Net Force (N)"], title="Force Breakdown", template="plotly_dark")
    st.plotly_chart(style_plot(fig_forces), use_container_width=True)

with row2_col2:
    fig_accel = px.line(sim_df, x="Time (s)", y="Acceleration (m/s²)", title="Acceleration Profile", template="plotly_dark")
    fig_accel.update_traces(line_color="#FFCC00")
    st.plotly_chart(style_plot(fig_accel), use_container_width=True)

st.subheader("Mass & Consumption Dynamics")
fig_mass = px.line(sim_df, x="Time (s)", y=["Total Mass (kg)", "Fuel Mass (kg)"], title="Mass Consumption Curves", template="plotly_dark")
st.plotly_chart(style_plot(fig_mass), use_container_width=True)

# ==========================================
# 5. RAW DATA TABLE
# ==========================================
with st.expander("View Raw Simulation Telemetry Data"):
    st.dataframe(sim_df)