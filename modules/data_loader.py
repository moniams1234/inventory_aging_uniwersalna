# modules/data_loader.py
# Handles file reading for xlsx, xls, csv with configurable header row

import pandas as pd
import streamlit as st
from io import BytesIO


def load_file_raw(uploaded_file) -> pd.DataFrame | None:
    """
    Load file without applying headers — used for raw preview so the user
    can choose which row contains column names.
    Returns DataFrame with default integer column indices.
    """
    try:
        filename = uploaded_file.name.lower()
        uploaded_file.seek(0)
        if filename.endswith(".csv"):
            for enc in ["utf-8", "cp1250", "latin-1"]:
                try:
                    uploaded_file.seek(0)
                    df = pd.read_csv(uploaded_file, encoding=enc, sep=None,
                                     engine="python", header=None)
                    return df
                except Exception:
                    continue
            return None
        elif filename.endswith(".xlsx"):
            return pd.read_excel(BytesIO(uploaded_file.read()), engine="openpyxl", header=None)
        elif filename.endswith(".xls"):
            return pd.read_excel(BytesIO(uploaded_file.read()), engine="xlrd", header=None)
        else:
            return None
    except Exception as e:
        st.error(f"Error loading file (raw): {e}")
        return None


def load_file(uploaded_file, header_row: int = 1) -> pd.DataFrame | None:
    """
    Load an uploaded file (xlsx, xls, csv) into a DataFrame.
    header_row: 1-based row number that contains column headers (default 1).
    Returns None on failure.
    """
    try:
        filename = uploaded_file.name.lower()
        # pandas header param is 0-based
        hdr = max(0, header_row - 1)

        if filename.endswith(".csv"):
            for enc in ["utf-8", "cp1250", "latin-1"]:
                try:
                    uploaded_file.seek(0)
                    raw_bytes = uploaded_file.read()
                    text = raw_bytes.decode(enc)
                    lines = text.splitlines()
                    if hdr >= len(lines):
                        return None
                    # Slice from the header row so sep-sniffing works correctly
                    from io import StringIO
                    sub = "\n".join(lines[hdr:])
                    df = pd.read_csv(StringIO(sub), sep=None, engine="python")
                    return df
                except Exception:
                    continue
            return None
        elif filename.endswith(".xlsx"):
            uploaded_file.seek(0)
            df = pd.read_excel(BytesIO(uploaded_file.read()), engine="openpyxl", header=hdr)
            return df
        elif filename.endswith(".xls"):
            uploaded_file.seek(0)
            df = pd.read_excel(BytesIO(uploaded_file.read()), engine="xlrd", header=hdr)
            return df
        else:
            return None
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None


def get_column_options(df: pd.DataFrame) -> list:
    """Return list of column names from DataFrame."""
    return [str(c) for c in df.columns]
