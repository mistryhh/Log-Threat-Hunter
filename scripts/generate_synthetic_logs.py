import pandas as pd
import random
from datetime import datetime, timedelta

def generate_logs(num_normal_records=1000):
    print("Generating normal log traffic...")
    logs = []
    users = [f"user_{i}" for i in range(1, 21)] # 20 standard users
    ips = [f"192.168.1.{random.randint(10, 100)}" for _ in range(30)] # Internal IPs

    # Start date
    start_time = datetime.now() - timedelta(days=7)

    # 1. Generate Normal Traffic
    for _ in range(num_normal_records):
        random_days = random.randint(0, 6)
        random_hours = random.randint(8, 17)
        random_minutes = random.randint(0, 59)
        random_seconds = random.randint(0, 59)

        timestamp = start_time + timedelta(days=random_days, hours=random_hours, minutes=random_minutes, seconds=random_seconds)

        user = random.choice(users)
        ip = random.choice(ips)

        # Most logins succeed normally, ocassionally fail due to wrong password
        status = "login_success" if random.random() > 0.1 else "login_failure"

        logs.append({
            "timestamp": timestamp,
            "ip_address": ip,
            "user": user,
            "status": status
        })

        # 2. Inject Anomaly 1: Brute Force Attack
        print("Injecting Brute-Force Attack...")
        attack_time = start_time + timedelta(days=2, hours=14, minutes=30)
        attacker_ip = "10.0.0.99" # Rougue IP address
        target_user = "user_5" # Victim User

        for _ in range(50): # Simulate 50 failed login attempts
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
    df.sort_values(by="timestamp").reset_index(drop=True)

    # Save to the data/raw folder
    output_path = "raw_server_logs.csv"
    df.to_csv(output_path, index=False)
    print(f"Successfully generated {len(df)} log records and saved to '{output_path}'.")

    if __name__ == "__main__":
        generate_logs()