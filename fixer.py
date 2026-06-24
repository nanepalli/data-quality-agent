import pandas as pd

def auto_fix(df):

    # Fix NULL names
    if "Name" in df.columns:
        df["Name"] = df["Name"].fillna("Unknown")

    # Remove negative ages
    if "Age" in df.columns:
        df = df[df["Age"] >= 0]

    # Remove invalid emails
    if "Email" in df.columns:
        df = df[
            df["Email"].astype(str).str.contains(
                r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                regex=True,
                na=False
            )
        ]

    # Remove duplicate emails
    if "Email" in df.columns:
        df = df.drop_duplicates(subset=["Email"])

    return df