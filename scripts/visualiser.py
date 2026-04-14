import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def create_visualizations():
    print("Generating Threat Hunting visualisations...\n")
    
    # 1. Load the Data
    file_path = os.path.join("..", "data", "raw", "raw_server_logs.csv")
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print("Error: Log file not found.")
        return

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Set up the output directory based on our folder structure
    output_dir = os.path.join("..", "outputs", "visualisations")
    os.makedirs(output_dir, exist_ok=True)

    # Set a professional visual style
    sns.set_theme(style="darkgrid")

    # --- PLOT 1: BRUTE-FORCE SPIKE ---
    plt.figure(figsize=(12, 6))
    failed_logins = df[df['status'] == 'login_failed'].copy()
    
    # Group failed logins by hour to see the massive spike
    failed_counts = failed_logins.set_index('timestamp').resample('1h').size()
    
    plt.plot(failed_counts.index, failed_counts.values, color='red', linewidth=2, marker='o')
    plt.title('Security Alert: Failed Login Attempts Over Time', fontsize=14, weight='bold')
    plt.xlabel('Date / Time', fontsize=12)
    plt.ylabel('Number of Failed Attempts', fontsize=12)
    plt.tight_layout()
    
    # Save the plot
    bf_path = os.path.join(output_dir, "brute_force_spike.png")
    plt.savefig(bf_path)
    plt.close()
    print(f"[*] Saved Brute Force visualisation to: {bf_path}")

    # --- PLOT 2: OFF-HOURS ACCESS DISTRIBUTION ---
    plt.figure(figsize=(10, 6))
    
    # Extract just the hour from the timestamp (0-23)
    df['hour'] = df['timestamp'].dt.hour
    successful_logins = df[df['status'] == 'login_success']
    
    # Create a histogram of login hours
    sns.histplot(successful_logins['hour'], bins=24, kde=False, color='steelblue')
    
    # Highlight the "Off-Hours" danger zone (Midnight to 5 AM)
    plt.axvspan(0, 5, color='red', alpha=0.2, label='Flagged Off-Hours (00:00 - 05:00)')
    
    plt.title('Access Patterns: Successful Logins by Hour of Day', fontsize=14, weight='bold')
    plt.xlabel('Hour of Day (0-23)', fontsize=12)
    plt.ylabel('Total Login Count', fontsize=12)
    plt.xticks(range(0, 24))
    plt.legend()
    plt.tight_layout()

    # Save the plot
    hours_path = os.path.join(output_dir, "login_hours_distribution.png")
    plt.savefig(hours_path)
    plt.close()
    print(f"[*] Saved Access Patterns visualisation to: {hours_path}")
    print("\nVisualizations complete! Check the 'outputs/visualisations/' folder.")

if __name__ == "__main__":
    create_visualizations()