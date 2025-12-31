import os
import sys
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

print(">>> Script started")

load_dotenv()
print(">>> .env file loaded")

print("DB_USER:", os.getenv("PG_USER"))
print("DB_NAME:", os.getenv("PG_DB"))
print("CSV Path:", os.path.exists("data/cleaned/all_parks_recreation_visits.csv"))

# ---------- CONFIG via .env ----------
DB_NAME = os.getenv("PG_DB", "tourism_project")
DB_USER = os.getenv("PG_USER", "capstone_user")
DB_PASS = os.getenv("PG_PASSWORD")           # no default for secrets
DB_HOST = os.getenv("PG_HOST", "localhost")
DB_PORT = os.getenv("PG_PORT", "5432")

CSV_PATH  = "data/cleaned/all_parks_recreation_visits.csv"
TABLE     = "park_visits"
SCHEMA    = "public"
CHUNK_SIZE = 50_000


# ------------------- FUNCTION DEFINITIONS -------------------

def make_engine():
    url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url, future=True)


def clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    # add cleaning logic if not already defined
    return df


def main():
    print(">>> step 1: validating CSV path")
    if not os.path.exists(CSV_PATH):
        print(f" CSV not found at {CSV_PATH}")
        sys.exit(1)

    print(">>> step 2: creating DB engine")
    engine = make_engine()

    print(">>> step 3: creating table/indexes if not exist")
    with engine.begin() as conn:
        conn.execute(text(DDL))

    print(">>> step 4: reading CSV")
    raw = pd.read_csv(CSV_PATH)

    print(">>> step 5: cleaning frame")
    df = clean_frame(raw)
    print(f">>> cleaned rows: {len(df):,}")

    print(f">>> step 6: upserting into public.park_visits")
    with engine.begin() as conn:
        # TEMP staging table (lives in session)
        conn.execute(text("CREATE TEMP TABLE park_visits_staging (LIKE public.park_visits INCLUDING ALL);"))

        # bulk insert to TEMP
        df.to_sql(name="park_visits_staging", con=conn, schema=None, if_exists="append", index=False)

        # merge (UPSERT) from TEMP → target
        conn.execute(text("""
            INSERT INTO public.park_visits (park, unit_code, park_type, region, state, year, month, recreation_visits)
            SELECT park, unit_code, park_type, region, state, year, month, recreation_visits
            FROM park_visits_staging
            ON CONFLICT (unit_code, year, month) DO UPDATE
            SET park              = EXCLUDED.park,
                park_type         = EXCLUDED.park_type,
                region            = EXCLUDED.region,
                state             = EXCLUDED.state,
                recreation_visits = EXCLUDED.recreation_visits;
        """))

    print(">>> done upserting")

# ---------- DDL (table & indexes) ----------
DDL = """
CREATE TABLE IF NOT EXISTS public.park_visits (
    id                  BIGSERIAL PRIMARY KEY,
    park                TEXT NOT NULL,
    unit_code           TEXT NOT NULL,
    park_type           TEXT NOT NULL,
    region              TEXT,
    state               TEXT,
    year                INT  NOT NULL CHECK (year BETWEEN 1900 AND 2100),
    month               INT  NOT NULL CHECK (month BETWEEN 1 AND 12),
    recreation_visits   BIGINT NOT NULL CHECK (recreation_visits >= 0)
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_park_month
ON public.park_visits (unit_code, year, month);

CREATE INDEX IF NOT EXISTS ix_state_year_month
ON public.park_visits (state, year, month);

CREATE INDEX IF NOT EXISTS ix_region_year
ON public.park_visits (region, year);

CREATE INDEX IF NOT EXISTS ix_park
ON public.park_visits (park);
"""

REQUIRED_COLS = [
    "Park", "Unit Code", "Park Type", "Region", "State",
    "Year", "Month", "Recreation Visits"
]

def clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = [c.strip() for c in df.columns]
    missing = [c for c in REQUIRED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"CSV is missing columns: {missing}")

    df = df[REQUIRED_COLS].copy()

    # strip text columns
    for c in ["Park", "Unit Code", "Park Type", "Region", "State"]:
        df[c] = df[c].astype(str).str.strip()

    # numeric
    df["Year"]  = pd.to_numeric(df["Year"], errors="coerce")
    df["Month"] = pd.to_numeric(df["Month"], errors="coerce")
    df["Recreation Visits"] = (
        df["Recreation Visits"].astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("\u2013", "0", regex=False)  # en-dash to zero if it appears
        .str.strip()
    )
    df["Recreation Visits"] = pd.to_numeric(df["Recreation Visits"], errors="coerce").fillna(0).astype("Int64")

    # drop invalid rows
    df = df.dropna(subset=["Year", "Month", "Recreation Visits"])
    df = df[(df["Month"].between(1, 12)) & (df["Year"].between(1900, 2100))]

    # rename to DB field names
    df = df.rename(columns={
        "Park": "park",
        "Unit Code": "unit_code",
        "Park Type": "park_type",
        "Region": "region",
        "State": "state",
        "Year": "year",
        "Month": "month",
        "Recreation Visits": "recreation_visits"
    })

    # dedupe within file
    df = df.drop_duplicates(subset=["unit_code", "year", "month"], keep="last")
    return df


# ------------------- ENTRY POINT -------------------
if __name__ == "__main__":
    try:
        print(">>> entering main()")
        main()
        print(">>> finished without errors")
    except Exception as e:
        import traceback
        traceback.print_exc()
