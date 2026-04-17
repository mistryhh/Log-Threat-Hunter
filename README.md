# Log-Threat-Hunter 🛡️

![Python](https://img.shields.io/badge/Python-%233776AB.svg?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-%23FF4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)

## 📖 Project Overview

This project is an **Automated Security Log Anomaly Detector** designed to simulate the detection, triage, and response to real-world cyber threats. 

Built to reflect the requirements of a 24/7 mission-critical Security Operations Center (SOC), this tool ingests raw server logs and applies data analysis to hunt for threat indicators. It automatically flags suspicious activity—such as brute-force attacks and unauthorized out-of-hours access—demonstrating how data engineering can be applied to front-line digital defense.

---

## 🖥️ Dashboard Preview

*(You can add a screenshot or GIF of your Streamlit dashboard here, just like you did for ESLM!)*
`![Threat Hunter Dashboard](./Threat_Hunter_Dashboard.gif)`

---

## 🚀 Key Threat Intelligence Discovered

* **Brute-Force Attack Detection:** Automatically identified high-velocity failed login attempts, aggregating failure counts by IP address to flag automated attacks (>10 failures per 5-minute window).
* **Off-Hours Access Monitoring:** Successfully isolated successful authentication events occurring outside of normal operating hours (00:00 - 05:00), allowing for rapid incident triage.
* **Interactive SOC Visualisation:** Transformed static CSV logs into a real-time, interactive threat dashboard to streamline the incident handling process.

---

## 📂 Repository Structure

```text
log-threat-hunter/
├── data/                      # (Git-ignored: Generated locally via script)
│   └── raw/                   # Raw synthetic server logs
├── scripts/                       
│   ├── generate_synthetic_logs.py # Step 1: Creates noisy system logs with injected anomalies
│   └── anomaly_detector.py        # Step 2: CLI-based threat hunting algorithm
├── app/                       
│   └── dashboard.py               # Step 3: Streamlit interactive SOC dashboard
├── requirements.txt           # Python dependencies
└── README.md