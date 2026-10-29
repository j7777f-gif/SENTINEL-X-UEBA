import pandas as pd
from pathlib import Path

DATA = Path(__import__("sys").argv[1]) if len(__import__("sys").argv) > 1 else Path("/mnt/hgfs/OpenSSH_2k.log_structured.csv")
OUTPUT = Path("/mnt/hgfs/ssh_baseline_features.csv")

df = pd.read_csv(DATA)

# Extract IPv4 addresses from log content
df["SourceIP"] = df["Content"].str.extract(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})"
)

# Identify authentication-related indicators
content = df["Content"].fillna("")
df["FailedAuth"] = content.str.contains(
    r"Failed password|authentication failure|Invalid user",
    case=False,
    regex=True
).astype(int)

df["InvalidUser"] = content.str.contains(
    "Invalid user", case=False, regex=False
).astype(int)

# Build a preliminary behavioral baseline per source IP
features = df.dropna(subset=["SourceIP"]).groupby("SourceIP").agg(
    EventCount=("EventId", "size"),
    UniqueEventTypes=("EventId", "nunique"),
    FailedAuthCount=("FailedAuth", "sum"),
    InvalidUserCount=("InvalidUser", "sum"),
).reset_index()

features["FailedAuthRate"] = (
    features["FailedAuthCount"] / features["EventCount"]
)

features.to_csv(OUTPUT, index=False)

print("Rows in original dataset:", len(df))
print("Rows with extracted IP:", df["SourceIP"].notna().sum())
print("Unique source IPs:", len(features))
print("\nTop source IPs by event count:")
print(features.sort_values("EventCount", ascending=False).head(10).to_string(index=False))
print("\nSaved features to:", OUTPUT)
