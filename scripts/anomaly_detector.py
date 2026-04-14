import pandas as pd
import os

def run_threat_hunt():
    print("Initializing Threat Hunt...\n")
    
    # 1. Load the Data
    file_path = os.path.join("..", "data", "raw", "raw_server_logs.csv")
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: Could not find {file_path}. Did you run the generator script first?")
        return

    # 2. Data Cleaning: Convert strings to actual Pandas Datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # --- THREAT HUNT 1: BRUTE-FORCE DETECTION ---
    # Looking for a high volume of failed logins from a single IP in a 5-minute window
    
    # Filter only failed logins
    failed_logins = df[df['status'] == 'login_failed'].copy()
    
    # Group by IP address and 5-minute intervals, then count them
    brute_force_suspects = failed_logins.groupby(
        ['ip_address', pd.Grouper(key='timestamp', freq='5min')]
    ).size().reset_index(name='failure_count')
    
    # Flag anything with more than 10 failures in that 5-minute window
    brute_force_alerts = brute_force_suspects[brute_force_suspects['failure_count'] > 10]
    
    print("--- BRUTE-FORCE ALERTS ---")
    if not brute_force_alerts.empty:
        print(brute_force_alerts.to_string(index=False))
    else:
        print("No brute-force activity detected.")
    print("\n")

    # --- THREAT HUNT 2: OFF-HOURS ACCESS ---
    # Looking for successful logins outside of typical working hours (e.g., Midnight to 5 AM)
    
    # Filter only successful logins
    successful_logins = df[df['status'] == 'login_success'].copy()
    
    # Extract the hour and find logins between midnight (0) and 5 AM (5)
    off_hours_alerts = successful_logins[
        (successful_logins['timestamp'].dt.hour >= 0) & 
        (successful_logins['timestamp'].dt.hour <= 5)
    ]
    
    print("--- OFF-HOURS ACCESS ALERTS ---")
    if not off_hours_alerts.empty:
        # Just selecting specific columns to keep the output clean
        print(off_hours_alerts[['timestamp', 'ip_address', 'user', 'status']].to_string(index=False))
    else:
        print("No off-hours access detected.")

if __name__ == "__main__":
    run_threat_hunt()