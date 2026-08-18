"""Structural comparison helpers for the raw PDS trial exports.

Reads column metadata only (no row data) so this is cheap to run across all
files. Pure structure comparison — column names/presence across trials —
not analysis of values. Feeds the harmonization mapping design in
dbt/models/staging/.
"""

from pathlib import Path

import pandas as pd
import pyreadstat

RAW_DOMAIN_TRIALS = [
    "NCT00115225_PACCE_bev_panitumumab_raw",
    "NCT00339183_panitumumab_folfiri_raw",
    "NCT00364013_panitumumab_folfox_raw",
]

ADAM_TRIALS = [
    "NCT00113763_panitumumab_bsc_ADaM",
    "NCT00364013_panitumumab_folfox_ADaM",
]


def list_columns(data_dir: Path, trial_folder: str, filename: str) -> list[str]:
    """Column names for one .sas7bdat file, without reading any row data."""
    path = data_dir / trial_folder / filename
    _, meta = pyreadstat.read_sas7bdat(str(path), metadataonly=True)
    return list(meta.column_names)


def presence_matrix(data_dir: Path, filename: str, trial_folders: list[str]) -> pd.DataFrame:
    """Column x trial boolean matrix for one domain filename (e.g. 'demo.sas7bdat')
    across a list of trial folders that all ship that same filename.
    """
    cols_by_trial = {t: set(list_columns(data_dir, t, filename)) for t in trial_folders}
    all_cols = sorted(set().union(*cols_by_trial.values()))
    matrix = pd.DataFrame(
        {t: [c in cols_by_trial[t] for c in all_cols] for t in trial_folders},
        index=all_cols,
    )
    matrix["n_trials_present"] = matrix.sum(axis=1)
    return matrix.sort_values("n_trials_present", ascending=False)


def columns_only(data_dir: Path, trial_folder: str, filename: str) -> pd.DataFrame:
    """One-column DataFrame of column names for a single file — for domains
    (like ADaM's adsl/adae) that don't share a common filename across trials,
    so a presence matrix isn't meaningful; just list them side by side by eye.
    """
    return pd.DataFrame({filename: list_columns(data_dir, trial_folder, filename)})
