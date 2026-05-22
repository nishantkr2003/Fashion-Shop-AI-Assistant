from pathlib import Path
import pandas as pd

ROOT = (
    Path(__file__).parent.parent.parent.parent
    / "Data"
    / "products"
)

def load_products():
    files = list(ROOT.glob("*.csv"))

    frames = []

    for f in files:
        frames.append(pd.read_csv(f))

    if not frames:
        return pd.DataFrame()

    return pd.concat(
        frames,
        ignore_index=True
    )