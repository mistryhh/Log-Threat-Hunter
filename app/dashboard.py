import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Threat Hunter Dashboard", page_icon="🛡️", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Load data from the data/raw folder (assuming we run this from the project root)
    file_path = os.path.join("data", "raw", "raw_server_logs.csv")
    try:
        df = pd.read_csv(file_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except FileNotFoundError:
        st.error(f"Error: Log file not found at {file_path}. Please run your generator script first.")
        st.stop()

df = load_data()

# --- ANOMALY DETECTION LOGIC ---
# 1. Create the 'hour' column on the main dataframe FIRST
df['hour'] = df['timestamp'].dt.hour

# 2. Separate failed and successful logins
failed_logins = df[df['status'] == 'login_failed'].copy()
successful_logins = df[df['status'] == 'login_success'].copy()

# 3. Detect Brute-Force Attempts (>10 failures in 5 mins)
brute_force_suspects = failed_logins.groupby(
    ['ip_address', pd.Grouper(key='timestamp', freq='5min')]
).size().reset_index(name='failure_count')
brute_force_alerts = brute_force_suspects[brute_force_suspects['failure_count'] > 10]

# 4. Detect Off-Hours Access (Midnight to 5 AM)
off_hours_alerts = successful_logins[(successful_logins['hour'] >= 0) & (successful_logins['hour'] <= 5)]

# --- DASHBOARD HEADER ---
st.title("🛡️ Cyber Security: Threat Hunter Dashboard")
st.markdown("""
*An interactive Security Operations Center (SOC) dashboard used to monitor server logs, detect brute-force attacks, and flag suspicious off-hours access.*
""")
st.divider()

# --- KPI METRICS ---
st.subheader("Live Security Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Logs Processed", f"{len(df):,}")
with col2:
    st.metric("Total Failed Logins", f"{len(failed_logins):,}")
with col3:
    st.metric("Brute-Force Incidents", len(brute_force_alerts), delta="High Risk Alert", delta_color="inverse")
with col4:
    st.metric("Off-Hours Logins", len(off_hours_alerts), delta="Requires Review", delta_color="inverse")

st.divider()

# --- CHARTS SECTION ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("🚨 Brute-Force Spikes")
    st.markdown("Visualising failed login attempts over time to spot automated attacks.")
    # Resample failed logins to 1-hour intervals for a cleaner line chart
    failed_counts = failed_logins.set_index('timestamp').resample('1h').size()
    st.line_chart(failed_counts)

with col_right:
    st.subheader("🌙 Access Patterns by Hour")
    st.markdown("Distribution of successful logins. Activity between 00:00 and 05:00 is flagged.")
    # Count successful logins by hour of the day
    hourly_success = successful_logins['hour'].value_counts().sort_index()
    st.bar_chart(hourly_success)

st.divider()

# --- DATA EXPLORER SECTION ---
st.subheader("🔍 Deep Dive: Active Threat Alerts")
st.markdown("Investigate the specific IP addresses and users triggering security alerts.")

col_bottom1, col_bottom2 = st.columns(2)

with col_bottom1:
    st.markdown("**Brute-Force Suspect IPs** (>10 failures in 5 mins)")
    if not brute_force_alerts.empty:
        st.dataframe(brute_force_alerts, use_container_width=True)
    else:
        st.success("No brute-force activity detected.")

with col_bottom2:
    st.markdown("**Suspicious Off-Hours Logins** (00:00 - 05:00)")
    if not off_hours_alerts.empty:
        st.dataframe(off_hours_alerts[['timestamp', 'ip_address', 'user', 'status']], use_container_width=True)
    else:
        st.success("No off-hours access detected.")