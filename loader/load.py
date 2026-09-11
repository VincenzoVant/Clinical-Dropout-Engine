"""One-shot loader: raw PDS domain exports (3 raw-domain trials) -> Postgres.

Deliberately dumb and mechanical — every original column is kept as-is, unrenamed, with only a
`trial_id` column added. All harmonization logic (renames, derived fields like `on_panitumumab`,
disposition-reason mapping, progression/censoring semantics) belongs in the dbt staging layer, not
here. See `learning-notes/docker.md` for how this fits into the Compose stack, and
`analytics/notebooks/` (4, 3, adam_mapping) for the harmonization findings this loader feeds into.
"""
import os
from pathlib import Path

import pandas as pd
import pyreadstat
from sqlalchemy import create_engine, text

RAW_DATA_DIR = Path(os.environ.get("RAW_DATA_DIR", "/data/raw"))

# NCT ID -> raw-domain export folder name. Only the 3 raw-domain trials ship demo/disposit/
# a_eendpt in this shape — the 2 ADaM-only trials (BSC, FOLFOX/PRIME ADaM) ship pre-derived adsl
# instead, out of scope for this pass.
TRIALS = {
    "NCT00115225": "NCT00115225_PACCE_bev_panitumumab_raw",
    "NCT00339183": "NCT00339183_panitumumab_folfiri_raw",
    "NCT00364013": "NCT00364013_panitumumab_folfox_raw",
}

# (source .sas7bdat filename, destination raw.<table> name)
DOMAINS = [
    ("demo.sas7bdat", "demo_raw"),
    ("disposit.sas7bdat", "disposit_raw"),
    ("a_eendpt.sas7bdat", "a_eendpt_raw"),
    ("ae.sas7bdat", "ae_raw"),
]


def build_engine():
    url = (
        f"postgresql+psycopg2://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
        f"@{os.environ['DB_HOST']}:{os.environ.get('DB_PORT', '5432')}/{os.environ['DB_NAME']}"
    )
    return create_engine(url)


def load_domain(engine, sas_filename, table_name):
    frames = []
    for trial_id, folder in TRIALS.items():
        path = RAW_DATA_DIR / folder / sas_filename
        df, _ = pyreadstat.read_sas7bdat(str(path))
        df.columns = [c.lower() for c in df.columns]
        df.insert(0, "trial_id", trial_id)
        frames.append(df)
        print(f"  {trial_id}: read {len(df)} rows from {path}")

    combined = pd.concat(frames, ignore_index=True)

    # pandas' if_exists="replace" issues a plain DROP TABLE, which Postgres refuses once a dbt
    # view (e.g. stg_demo) depends on this table — and since postgres-data is a named volume,
    # that view survives across `docker compose up`/`down` cycles. Drop with CASCADE ourselves
    # first so re-running the loader stays idempotent even after dbt has built on top of it.
    with engine.begin() as conn:
        conn.execute(text(f"DROP TABLE IF EXISTS raw.{table_name} CASCADE"))

    combined.to_sql(table_name, engine, schema="raw", if_exists="append", index=False)
    print(f"Loaded {len(combined)} total rows into raw.{table_name}")


if __name__ == "__main__":
    engine = build_engine()

    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS raw"))

    for sas_filename, table_name in DOMAINS:
        print(f"--- {table_name} ---")
        load_domain(engine, sas_filename, table_name)
