import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
OUT_DIR = Path("data/cleaned")
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_FILE = OUT_DIR / "all_parks_recreation_visits.csv"

REQUIRED = ["Park","Unit Code","Park Type","Region","State","Year","Month","Recreation Visits"]

csvs = sorted(RAW_DIR.glob("*.csv"))
print(f"Found {len(csvs)} CSV files to merge...")

frames = []
for fp in csvs:
    try:
        # Be forgiving about weird rows & commas in numbers
        df = pd.read_csv(
            fp,
            dtype=str,
            engine="python",
            on_bad_lines="skip",
            sep=None
        )

        # If headers are missing or wrong, try to coerce
        cols = [c.strip() for c in df.columns.tolist()]
        if len(cols) >= 8:
            df = df.iloc[:, :8]
            df.columns = REQUIRED
        elif set(REQUIRED).issubset(set(cols)):
            df = df[REQUIRED]
        else:
            print(f"  Skipping {fp}: Missing required columns")
            continue

        # Clean numbers like 1,23,456 → 123456
        df["Recreation Visits"] = (
            df["Recreation Visits"].astype(str)
            .str.replace(r"[^0-9]", "", regex=True)
        )

        # Coerce Year/Month to int; drop bad rows
        df["Year"] = pd.to_numeric(df["Year"], errors="coerce")
        df["Month"] = pd.to_numeric(df["Month"], errors="coerce")
        df["Recreation Visits"] = pd.to_numeric(df["Recreation Visits"], errors="coerce")
        df = df.dropna(subset=["Year","Month","Recreation Visits"])
        df["Year"] = df["Year"].astype(int)
        df["Month"] = df["Month"].astype(int)

        # Trim text columns
        for c in ["Park","Unit Code","Park Type","Region","State"]:
            df[c] = df[c].astype(str).str.strip()

        frames.append(df)

    except Exception as e:
        print(f"  Error reading {fp}: {e}")

if not frames:
    raise SystemExit("No valid CSVs were processed!")

merged = pd.concat(frames, ignore_index=True)
# Basic sanity
merged = merged[(merged["Month"] >= 1) & (merged["Month"] <= 12)]

merged.to_csv(OUT_FILE, index=False)
print(f" Wrote {OUT_FILE} with {len(merged):,} rows from {len(frames)} usable files.")
