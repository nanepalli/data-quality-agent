import pandas as pd
import yaml


def run_checks(csv_file):

    df = pd.read_csv(csv_file)

    with open("rules.yaml", "r") as file:
        rules = yaml.safe_load(file)

    issues = []

    for check in rules["checks"]:

        column = check["column"]
        check_type = check["type"]

        # NULL CHECK
        if check_type == "not_null":

            bad_rows = df[df[column].isnull()]

            if not bad_rows.empty:
                issues.append({
                    "issue": f"{column.capitalize()} contains NULL values",
                    "rows": bad_rows
                })

        # NEGATIVE VALUE CHECK
        elif check_type == "positive":

            bad_rows = df[df[column] < 0]

            if not bad_rows.empty:
                issues.append({
                    "issue": f"{column.capitalize()} contains negative values",
                    "rows": bad_rows
                })

        # EMAIL FORMAT CHECK
        elif check_type == "email":

            bad_rows = df[
                ~df[column].astype(str).str.contains(
                    r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
                    regex=True,
                    na=False
                )
            ]

            if not bad_rows.empty:
                issues.append({
                    "issue": f"{column.capitalize()} contains invalid email addresses",
                    "rows": bad_rows
                })

        # DUPLICATE CHECK
        elif check_type == "unique":

            bad_rows = df[df[column].duplicated(keep=False)]

            if not bad_rows.empty:
                issues.append({
                    "issue": f"{column.capitalize()} contains duplicate values",
                    "rows": bad_rows
                })

    return issues