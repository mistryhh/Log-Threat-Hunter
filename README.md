# Log-Threat-Hunter: Automated Security Log Anomaly Detector

## Project Overview
This project simulates a Cyber Security Threat Hunting pipeline. It automatically ingests, cleans, and analyses system login logs to detect suspicious behavior. Built specifically to demonstrate operational security awareness, data manipulation with **Pandas**, and automated anomaly detection.

The tool identifies two primary threat vectors:
1. **Brute-Force Attacks:** High-frequency failed login attempts from a single IP address within a rolling 5-minute window.
2. **Suspicious Off-Hours Access:** Successful user logins occurring outside of standard organisational working hours (00:00 - 05:00).

## Repository Structure
```text
Log-Threat-Hunter/
│
├── scripts/
│   ├── generate_synthetic_logs.py  # Generates realistic simulated log data
│   ├── anomaly_detector.py         # Pandas-based threat hunting logic
│   └── visualiser.py               # Generates Matplotlib/Seaborn dashboards
│
├── .gitignore                      # Prevents raw data from being committed
├── requirements.txt                # Python dependencies
└── README.md                       # Project documentation
```

## Technology Stack
![Python](https://img.shields.io/badge/Python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)

* **Pandas:** For handling missing values, time-series transformations, and data aggregation.
* **Matplotlib & Seaborn:** For generating professional security dashboards.

## Setup & Installation
1. Clone the Repository:
```bash
git clone https://github.com/mistryhh/Log-Threat-Hunter.git
cd Log-Threat-Hunter
```
2. Install Required Dependancies:
```bash
pip install -r requirements.txt
```

## Usage: Running the Pipeline
1. **Generate Simulated Logs**:
Because real security logs are sensitive and should never be public, this script generates a realistic synthetic dataset (`raw_server_logs.csv`) containing normal traffic and injected threats.
```bash
cd scripts
python generate_synthetic_logs.py
```
2. **Run the Threat Hunter**: 
This script parses the logs, converts timestamps, and isolates the anomalous IP addresses and users.
```bash
python anomaly_detector.py
```
3. **Generate Visual Dashboards**: This script creates visual representations of the flagged data to aid security analysts in reporting.
```bash
python visualiser.py
```

Once Running all these scripts you should see two images in the `outputs/visualisations` folder. These images are the visual representations of the Brute Force and Access Patterns.

## Results & Visualisations
1. **Brute-Force Detection**:
The system successfully flags an isolated IP address (10.0.0.99) executing over 50 failed login attempts in a localised time window.

![Brute Force Spike](examples\brute_force_spike.png)

2. **Off-Hours Access Patterns**:
The time-series histogram categorises successful logins by hour, highlighting the anomalies in the red "Flagged Off-Hours" zone.

![Access Patterns](examples\login_hours_distribution.png)

## Key Learnings
* **Defensive Programming:** Implementing try/except blocks and dynamic folder generation ensures the tool runs reliably on different environments.
* **Data Privacy:** Utilising `.gitignore` to prevent simulated (or real) server logs from leaking into public repositories.
* **Time-Series Analysis:** Leveraging pd.Grouper for efficient, memory-safe rolling timeframe analysis.
