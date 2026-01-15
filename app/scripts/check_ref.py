import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path


# =========================
BASE_DIR = Path(__file__).resolve().parent.parent  

INPUT_PATH = BASE_DIR / "data" / "referential" / "books.csv"
OUTPUT_PATH = BASE_DIR / "data" / "referential" / "books_clean.csv"
MAX_ROWS = 500

CURRENT_YEAR = datetime.now().year

df = pd.read_csv(INPUT_PATH, engine="python", on_bad_lines="skip", skipinitialspace=True)
df.columns = [str(col).strip() for col in df.columns]

for col in df.select_dtypes(include=["object"]).columns:
    df[col] = df[col].fillna("").astype(str).str.strip()

def clean_year(year):
    try:
        year = int(year)
        if year > CURRENT_YEAR:
            return np.nan
        return year
    except:
        return np.nan

df["publication_year"] = df["publication_year"].apply(clean_year)


invalid_years = df["publication_year"].isna().sum()

def year_to_period(year):
    if pd.isna(year):
        return "Unknown"
    if year < 1900:
        return "Classic"
    elif year <= 1945:
        return "Early 20th Century"
    elif year <= 1980:
        return "Late 20th Century"
    elif year <= 2000:
        return "Contemporary"
    else:
        return "Modern"

df["period"] = df["publication_year"].apply(year_to_period)

for col in ["title", "author", "genres"]:
    if col in df.columns:
        df[col] = df[col].str.lower()


duplicate_mask = df.duplicated(subset=["title", "author"])
df = df[~duplicate_mask]

df_final = df.head(MAX_ROWS)

df_final.to_csv(OUTPUT_PATH, index=False)

print(f"\nClean dataset exported to: {OUTPUT_PATH}")
