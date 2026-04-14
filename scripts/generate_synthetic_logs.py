import pandas as pd
import random
from datetime import datetime, timedelta
import os

def generate_logs(num_normal_records=1000):
    print("Generating normal log traffic...")
    logs = []
    users = [f"user_{i}" for i in range(1, 21)]  # 20 standard users
    ips = [f"192.168.1.{random.randint(10, 100)}" for _ in range(30)] # Internal IPs
    
    # Start date: A week ago
    start_time = datetime.now() - timedelta(days=7)
    
    # 1. Generate Normal Traffic
    for _ in range(num_normal_records):
        # Random time within normal working hours
        random_days = random.randint(0, 6)
        random_hours = random.randint(8, 17)
        random_minutes = random.randint(0, 59)
        random_seconds = random.randint(0, 59)
        
        timestamp = start_time + timedelta(days=random_days, hours=random_hours, minutes=random_minutes, seconds=random_seconds)
        
        user = random.choice(users)
        ip = random.choice(ips)
        
        # Most logins succeed normally, occasionally people type the wrong password
        status = "login_success" if random.random() > 0.1 else "login_failed"
        
        logs.append({
            "timestamp": timestamp,
            "ip_address": ip,
            "user": user,
            "status": status
        })

    # 2. Inject Anomaly 1: Brute Force Attack
    print("Injecting Brute-Force Attack...")
    attack_time = start_time + timedelta(days=2, hours=14, minutes=30)
    attacker_ip = "10.0.0.99"  # Rogue IP
    target_user = "user_5"     
    
    # 50 failed attempts in 2 minutes
    for _ in range(50):
        attack_time += timedelta(seconds=random.randint(1, 3))
        logs.append({
            "timestamp": attack_time,
            "ip_address": attacker_ip,
            "user": target_user,
            "status": "login_failed"
        })

    # 3. Inject Anomaly 2: Suspicious Off-Hours Access
    print("Injecting Off-Hours Access...")
    sneaky_time = start_time + timedelta(days=4, hours=3, minutes=15) 
    logs.append({
        "timestamp": sneaky_time,
        "ip_address": "192.168.1.45",
        "user": "user_12", 
        "status": "login_success" 
    })

    # Create DataFrame and sort chronologically
    df = pd.DataFrame(logs)
    df = df.sort_values(by="timestamp").reset_index(drop=True)
    
    # Navigate up one level from 'scripts', then into 'data/raw'
    output_dir = os.path.join("..", "data", "raw")
    
    # Tell Python to automatically create these folders if they don't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Combine the folder path and the file name
    output_path = os.path.join(output_dir, "raw_server_logs.csv")
    
    # Save to the data/raw folder
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {len(df)} log records and saved to '{output_path}'.")

if __name__ == "__main__":
    generate_logs()