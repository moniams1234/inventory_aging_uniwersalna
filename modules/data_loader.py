# modules/data_loader.py
# Handles file reading for xlsx, xls, csv

import pandas as pd
import streamlit as st
from io import BytesIO


def load_file(uploaded_file) -> pd.DataFrame | None:
    """
    Load an uploaded file (xlsx, xls, csv) into a DataFrame.
    Returns None on failure.
    """
    try:
        filename = uploaded_file.name.lower()
        if filename.endswith(".csv"):
            # Try common encodings
            for enc in ["utf-8", "cp1250", "latin-1"]:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=enc, sep=None, engine="python")
                    return df
                except Exception:
                    continue
            return None
        elif filename.endswith(".xlsx"):
            uploaded_file.seek(0)
            df = pd.read_excel(BytesIO(uploaded_file.read()), engine="openpyxl")
            return df
        elif filename.endswith(".xls"):
            uploaded_file.seek(0)
            df = pd.read_excel(BytesIO(uploaded_file.read()), engine="xlrd")
            return df
        else:
            return None
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def get_column_options(df: pd.DataFrame) -> list:
    """Return list of column names from DataFrame."""
    return list(df.columns)
