import pandas as pd
import os

def analyze_data(filepath):
    if filepath.endswith(".csv"):
        df = pd.read_csv(filepath)
    else:
        df = pd.read_excel(filepath)
    summary = df.describe(include='all').fillna('').to_dict()
    return summary

def load_dataframe(filepath):
    if filepath.endswith(".csv"):
        return pd.read_csv(filepath)
    else:
        return pd.read_excel(filepath)
