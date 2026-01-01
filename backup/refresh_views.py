from sqlalchemy import text
from src.db import get_engine

VIEWS = [
    "mv_state_month_visits",
    "mv_region_month_visits",
    "mv_park_yearly_totals",
    "mv_park_yoy",
]

def main():
    engine = get_engine()
    with engine.begin() as conn:
        for v in VIEWS:
            conn.execute(text(f"REFRESH MATERIALIZED VIEW CONCURRENTLY public.{v};"))
            print(f"Refreshed: public.{v}")

if __name__ == "__main__":
    main()
    print("All materialized views refreshed.")

