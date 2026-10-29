import pandas as pd
from pathlib import Path

INPUT = Path(__import__("sys").argv[1]) if len(__import__("sys").argv) > 1 else Path("/mnt/hgfs/ssh_isolation_results.csv")
OUTPUT = Path("/mnt/hgfs/ssh_dynamic_risk_results.csv")

df = pd.read_csv(INPUT)

# Normalize event volume to a 0-100 scale using log scaling
log_volume = __import__("numpy").log1p(df["EventCount"])
max_volume = log_volume.max()

if max_volume > 0:
    df["VolumeScore"] = 100 * log_volume / max_volume
else:
    df["VolumeScore"] = 0.0

# Convert distinct event types into a 0-100 score
max_types = df["UniqueEventTypes"].max()
if max_types > 0:
    df["DiversityScore"] = 100 * df["UniqueEventTypes"] / max_types
else:
    df["DiversityScore"] = 0.0

# Authentication failure indicator rate
df["AuthFailureScore"] = 100 * df["FailedAuthRate"].clip(0, 1)

# Isolation Forest score: flagged anomalies receive a higher score
df["AnomalyScoreComponent"] = (
    df["AnomalyLabel"].eq(-1).astype(float) * 100
)

# Transparent weighted score; weights sum to 1
df["RiskScore"] = (
    0.35 * df["AuthFailureScore"]
    + 0.30 * df["VolumeScore"]
    + 0.10 * df["DiversityScore"]
    + 0.25 * df["AnomalyScoreComponent"]
).clip(0, 100).round(2)

def risk_level(score):
    if score >= 75:
        return "High"
    if score >= 40:
        return "Medium"
    return "Low"

df["RiskLevel"] = df["RiskScore"].apply(risk_level)

df = df.sort_values("RiskScore", ascending=False)
df.to_csv(OUTPUT, index=False)

print("Total IPs scored:", len(df))
print("\nHighest risk scores:")
print(
    df[["SourceIP", "EventCount", "FailedAuthRate",
        "AnomalyStatus", "RiskScore", "RiskLevel"]]
    .head(10)
    .to_string(index=False)
)
print("\nSaved results to:", OUTPUT)
