-- ===============================
-- TOURISM PROJECT: ANALYTICS VIEWS
-- ===============================

-- State x Month totals (for heatmaps)
CREATE MATERIALIZED VIEW IF NOT EXISTS public.mv_state_month_visits AS
SELECT
    state,
    year,
    month,
    SUM(recreation_visits) AS visits
FROM public.park_visits
GROUP BY state, year, month;

-- Unique index required for CONCURRENTLY refresh
CREATE UNIQUE INDEX IF NOT EXISTS ux_mv_state_month_unique
ON public.mv_state_month_visits (state, year, month);

-- Region x Month totals
CREATE MATERIALIZED VIEW IF NOT EXISTS public.mv_region_month_visits AS
SELECT
    COALESCE(region, 'Unknown') AS region,
    year,
    month,
    SUM(recreation_visits) AS visits
FROM public.park_visits
GROUP BY COALESCE(region, 'Unknown'), year, month;

CREATE UNIQUE INDEX IF NOT EXISTS ux_mv_region_month_unique
ON public.mv_region_month_visits (region, year, month);

-- Park yearly totals
CREATE MATERIALIZED VIEW IF NOT EXISTS public.mv_park_yearly_totals AS
SELECT
    unit_code,
    park,
    year,
    SUM(recreation_visits) AS visits_year
FROM public.park_visits
GROUP BY unit_code, park, year;

CREATE UNIQUE INDEX IF NOT EXISTS ux_mv_park_yearly_unique
ON public.mv_park_yearly_totals (unit_code, year);

-- Year-over-Year growth (%)
CREATE MATERIALIZED VIEW IF NOT EXISTS public.mv_park_yoy AS
WITH base AS (
    SELECT unit_code, park, year, SUM(recreation_visits) AS visits_year
    FROM public.park_visits
    GROUP BY unit_code, park, year
),
yoy AS (
    SELECT
        unit_code,
        park,
        year,
        visits_year,
        LAG(visits_year) OVER (PARTITION BY unit_code ORDER BY year) AS prev_year
    FROM base
)
SELECT
    unit_code,
    park,
    year,
    visits_year,
    CASE
        WHEN prev_year IS NULL OR prev_year = 0 THEN NULL
        ELSE ROUND(100.0 * (visits_year - prev_year) / prev_year, 2)
    END AS yoy_pct
FROM yoy;

CREATE UNIQUE INDEX IF NOT EXISTS ux_mv_park_yoy_unique
ON public.mv_park_yoy (unit_code, year);


-- REFRESH COMMANDS (run manually after loading new data)
-- REFRESH MATERIALIZED VIEW CONCURRENTLY public.mv_state_month_visits;
-- REFRESH MATERIALIZED VIEW CONCURRENTLY public.mv_region_month_visits;
-- REFRESH MATERIALIZED VIEW CONCURRENTLY public.mv_park_yearly_totals;
-- REFRESH MATERIALIZED VIEW CONCURRENTLY public.mv_park_yoy;

-- END OF FILE



