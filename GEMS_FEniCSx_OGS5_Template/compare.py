"""Comparison tables used by the case scripts (pandas only)."""
from pathlib import Path
import numpy as np
import pandas as pd


def error_table(ours, ref, keys=None):
    """Max absolute / relative difference between ours[k] and ref[k] for every common key.

    Relative = max |ours - ref| / max |ref|."""
    rows = []
    for k in (keys or [k for k in ref if k in ours]):
        a, b = np.asarray(ours[k], float), np.asarray(ref[k], float)
        scale = np.abs(b).max()
        rows.append({'quantity': k, 'ref_max': scale, 'max_abs_diff': np.abs(a - b).max(),
                     'max_rel_diff': np.abs(a - b).max() / scale if scale > 0 else np.nan})
    return pd.DataFrame(rows)


def compare_previous(ours, previous_file, rename=lambda k: k, keys=None):
    """Compare with the result file of the earlier stand-alone notebook, if it is there.

    Prints the largest relative difference per quantity; returns the table or None."""
    previous_file = Path(previous_file)
    if not previous_file.exists():
        print(f'(earlier notebook result {previous_file.name} not found, skipped)')
        return None
    prev = pd.read_csv(previous_file) if previous_file.suffix == '.csv' else dict(np.load(previous_file, allow_pickle=True))
    keys = keys or [k for k in ours if rename(k) in prev]
    table = error_table({k: ours[k] for k in keys}, {k: np.asarray(prev[rename(k)]) for k in keys})
    print(f'\nvs earlier notebook ({previous_file.parent.parent.name}): '
          f'largest relative difference {table.max_rel_diff.max():.2e}')
    print(table.to_string(index=False))
    return table
