import streamlit as st
from checker import run_checks
from fixer import auto_fix
import pandas as pd

st.set_page_config(
    page_title="Data Quality Agent",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Data Quality Agent")


uploaded_file = st.file_uploader(
    "Upload a CSV or Parquet file",
    type=["csv", "parquet"]
)

if uploaded_file is not None:

    # Read uploaded file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif uploaded_file.name.endswith(".parquet"):
        df = pd.read_parquet(uploaded_file)

    # Show uploaded data
    st.subheader("📁 Uploaded Data")
    st.dataframe(df, use_container_width=True)

    # Save temporary file
    temp_file = "uploaded_data.csv"
    df.to_csv(temp_file, index=False)

    # Run checks
    issues = run_checks(temp_file)
    # Show uploaded data
    st.subheader("📁 Uploaded Data")
    st.dataframe(df, use_container_width=True)

    # Save temporary file
    temp_file = "uploaded_data.csv"
    df.to_csv(temp_file, index=False)

    # Run checks
    issues = run_checks(temp_file)

    # Data Quality Report
    st.subheader("📋 Data Quality Report")

    total_checks = 5
    score = max(
        0,
        ((total_checks - len(issues)) / total_checks) * 100
    )

    st.metric(
        "Data Quality Score",
        f"{score:.0f}%"
    )

    if score >= 80:
        st.success("✅ Good Data Quality")
    elif score >= 50:
        st.warning("⚠️ Moderate Data Quality")
    else:
        st.error("❌ Poor Data Quality")

    # Show Issues
    if issues:

        st.write(f"### Total Issues Found: {len(issues)}")

        report_lines = []

        for item in issues:

            st.error(item["issue"])

            report_lines.append(item["issue"])

            st.write("Bad Rows:")

            st.dataframe(
                item["rows"],
                use_container_width=True
            )

            # Fix Suggestions
            if st.button(
                f"Show Fix - {item['issue']}"
            ):

                if "NULL" in item["issue"]:

                    st.info("""
Suggested Fix

Pandas:
df["Name"] = df["Name"].fillna("Unknown")

SQL:
UPDATE customers
SET Name='Unknown'
WHERE Name IS NULL;
""")

                elif "negative" in item["issue"]:

                    st.info("""
Suggested Fix

Pandas:
df = df[df["Age"] >= 0]

SQL:
DELETE FROM customers
WHERE Age < 0;
""")

                elif "invalid email" in item["issue"]:

                    st.info("""
Suggested Fix

Pandas:
df = df[df["Email"].str.contains("@")]

SQL:
DELETE FROM customers
WHERE Email NOT LIKE '%@%';
""")

                elif "duplicate" in item["issue"]:

                    st.info("""
Suggested Fix

Pandas:
df = df.drop_duplicates(subset=["Email"])

SQL:
Remove duplicate email records.
""")

        report_text = "\n".join(report_lines)

        st.download_button(
            label="📥 Download Report",
            data=report_text,
            file_name="data_quality_report.txt",
            mime="text/plain"
        )

    else:
        st.success("🎉 No data quality issues found!")

    # ==========================
    # AUTO FIX SECTION
    # ==========================

    st.subheader("🔧 Auto Fix Data")

    if st.button("Apply Auto Fix"):

        fixed_df = auto_fix(df)

        original_rows = len(df)
        cleaned_rows = len(fixed_df)
        removed_rows = original_rows - cleaned_rows

        st.success("✅ Data cleaned successfully!")

        st.write(f"Original Rows: {original_rows}")
        st.write(f"Rows After Cleaning: {cleaned_rows}")
        st.write(f"Rows Removed: {removed_rows}")

        st.subheader("📄 Cleaned Data")

        st.dataframe(
            fixed_df,
            use_container_width=True
        )

        st.download_button(
            label="📥 Download Cleaned CSV",
            data=fixed_df.to_csv(index=False),
            file_name="cleaned_data.csv",
            mime="text/csv"
        )