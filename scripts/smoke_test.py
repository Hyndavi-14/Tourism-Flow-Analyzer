import pandas as pd
from sqlalchemy import text
from src.db import get_engine

def show(title, df, n=5):
    print(f"\n=== {title} (top {n}) ===")
    print(df.head(n).to_string(index=False))

def main():
    engine = get_engine()

    with engine.begin() as conn:
        # 1) Recent state-month leaders
        q1 = text("""
            SELECT state, year, month, visits
            FROM public.mv_state_month_visits
            WHERE year = (SELECT MAX(year) FROM public.mv_state_month_visits)
            ORDER BY visits DESC
            LIMIT 10;
        """)
        df1 = pd.read_sql(q1, conn)
        show("Top states (latest year)", df1)

        # 2) YoY growth leaders
        q2 = text("""
            SELECT unit_code, park, year, yoy_pct, visits_year
            FROM public.mv_park_yoy
            WHERE yoy_pct IS NOT NULL
            ORDER BY yoy_pct DESC
            LIMIT 10;
        """)
        df2 = pd.read_sql(q2, conn)
        show("Fastest growing parks (YoY)", df2)

        # 3) Simple row count sanity check
        q3 = text("SELECT COUNT(*) AS rows FROM public.park_visits;")
        df3 = pd.read_sql(q3, conn)
        show("Raw table row count", df3, n=1)

if __name__ == "__main__":
    main()

