import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

INPUT = __import__("sys").argv[1] if len(__import__("sys").argv) > 1 else "/mnt/hgfs/ssh_baseline_features.csv"
OUTPUT = "/mnt/hgfs/ssh_isolation_results.csv"

df = pd.read_csv(INPUT)

columns = [
    "EventCount",
    "UniqueEventTypes",
    "FailedAuthCount",
    "InvalidUserCount",
    "FailedAuthRate",
]

X = df[columns].fillna(0)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = IsolationForest(
    n_estimators=200,
    contamination=0.15,
    random_state=42
)

df["AnomalyLabel"] = model.fit_predict(X_scaled)
df["AnomalyScore"] = model.decision_function(X_scaled)
df["AnomalyStatus"] = df["AnomalyLabel"].map({
    -1: "Anomaly",
    1: "Normal"
})

df = df.sort_values("AnomalyScore")

df.to_csv(OUTPUT, index=False)

print("Total IPs:", len(df))
print("Flagged anomalies:", (df["AnomalyLabel"] == -1).sum())
print("\nLowest anomaly scores:")
print(
    df[["SourceIP", "EventCount", "FailedAuthRate",
        "AnomalyScore", "AnomalyStatus"]]
    .head(10)
    .to_string(index=False)
)
print("\nSaved results to:", OUTPUT)
