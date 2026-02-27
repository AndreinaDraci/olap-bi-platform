"""
Database module: loads CSV into DuckDB in-memory star schema.
Provides a connection and helper query functions.
"""
import os
import duckdb
import pandas as pd

_conn = None
_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "global_retail_sales.csv")


def get_connection() -> duckdb.DuckDBPyConnection:
    global _conn
    if _conn is None:
        _conn = duckdb.connect(database=":memory:")
        _init_schema(_conn)
    return _conn


def _init_schema(conn: duckdb.DuckDBPyConnection):
    """Load CSV and build star schema."""
    csv_path = os.path.abspath(_CSV_PATH)

    # Load raw data
    conn.execute(f"""
        CREATE TABLE raw_sales AS
        SELECT * FROM read_csv_auto('{csv_path}')
    """)

    # ── Dimension tables ────────────────────────────────────────────────────
    conn.execute("""
        CREATE TABLE dim_date AS
        SELECT DISTINCT
            order_date,
            year,
            quarter,
            month,
            month_name
        FROM raw_sales
        ORDER BY order_date
    """)

    conn.execute("""
        CREATE TABLE dim_geography AS
        SELECT DISTINCT
            region,
            country
        FROM raw_sales
        ORDER BY region, country
    """)

    conn.execute("""
        CREATE TABLE dim_product AS
        SELECT DISTINCT
            category,
            subcategory
        FROM raw_sales
        ORDER BY category, subcategory
    """)

    conn.execute("""
        CREATE TABLE dim_customer AS
        SELECT DISTINCT
            customer_segment
        FROM raw_sales
        ORDER BY customer_segment
    """)

    # ── Fact table ──────────────────────────────────────────────────────────
    conn.execute("""
        CREATE TABLE fact_sales AS
        SELECT
            order_id,
            order_date,
            year,
            quarter,
            month,
            month_name,
            region,
            country,
            category,
            subcategory,
            customer_segment,
            quantity,
            unit_price,
            revenue,
            cost,
            profit,
            profit_margin
        FROM raw_sales
    """)

    conn.execute("DROP TABLE raw_sales")

    print("[DB] Star schema initialized ✓")
    print(f"[DB] fact_sales rows: {conn.execute('SELECT COUNT(*) FROM fact_sales').fetchone()[0]:,}")


def query(sql: str) -> pd.DataFrame:
    """Execute a SQL query and return a DataFrame."""
    conn = get_connection()
    return conn.execute(sql).df()


def get_schema_info() -> dict:
    """Return schema metadata for agent context."""
    conn = get_connection()
    info = {}
    for table in ["fact_sales", "dim_date", "dim_geography", "dim_product", "dim_customer"]:
        cols = conn.execute(f"PRAGMA table_info({table})").df()
        info[table] = cols[["name", "type"]].to_dict("records")
    return info


DDL_SCRIPTS = """
-- Star Schema DDL (DuckDB / PostgreSQL compatible)

CREATE TABLE dim_date (
    order_date  DATE PRIMARY KEY,
    year        INTEGER,
    quarter     VARCHAR(2),
    month       INTEGER,
    month_name  VARCHAR(20)
);

CREATE TABLE dim_geography (
    region   VARCHAR(50),
    country  VARCHAR(50),
    PRIMARY KEY (region, country)
);

CREATE TABLE dim_product (
    category     VARCHAR(50),
    subcategory  VARCHAR(50),
    PRIMARY KEY (category, subcategory)
);

CREATE TABLE dim_customer (
    customer_segment VARCHAR(50) PRIMARY KEY
);

CREATE TABLE fact_sales (
    order_id          VARCHAR(20) PRIMARY KEY,
    order_date        DATE REFERENCES dim_date(order_date),
    year              INTEGER,
    quarter           VARCHAR(2),
    month             INTEGER,
    month_name        VARCHAR(20),
    region            VARCHAR(50),
    country           VARCHAR(50),
    category          VARCHAR(50),
    subcategory       VARCHAR(50),
    customer_segment  VARCHAR(50) REFERENCES dim_customer(customer_segment),
    quantity          INTEGER,
    unit_price        DECIMAL(10,2),
    revenue           DECIMAL(12,2),
    cost              DECIMAL(12,2),
    profit            DECIMAL(12,2),
    profit_margin     DECIMAL(5,2)
);
"""
