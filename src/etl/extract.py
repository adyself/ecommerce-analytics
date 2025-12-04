from pathlib import Path
import pandas as pd


def load_csv(name: str):
    # Корень проекта: ...\ecommerce-analytics
    project_root = Path(__file__).resolve().parents[2]

    # Сырые данные — в data/raw
    base = project_root / "data" / "raw"
    path = base / name

    if not path.exists():
        raise FileNotFoundError(f"Cannot find {name} in {base}")

    return pd.read_csv(path)
