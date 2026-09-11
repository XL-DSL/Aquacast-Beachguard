from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parent.parent
PREDICTION_CSV = ROOT / "data" / "app_predictions.csv"

APP_VERSION = "V2.1-LIVE"

VALID_RISKS = {
    "Safe",
    "Caution",
    "Unsafe",
}

RISK_RANK = {
    "Safe": 0,
    "Caution": 1,
    "Unsafe": 2,
}

REQUIRED_COLUMNS = [
    "site_id",
    "site_name",
    "prediction_date",
    "data_last_updated",
    "e_coli_probability",
    "enterococcus_probability",
    "e_coli_risk",
    "enterococcus_risk",
    "overall_risk",
    "model_version",
]


def classify_risk(bacteria, probability):
    probability = float(probability)

    if bacteria == "E. coli":
        if probability < 0.10:
            return "Safe"
        if probability < 0.50:
            return "Caution"
        return "Unsafe"

    if bacteria == "Enterococcus":
        if probability < 0.40:
            return "Safe"
        if probability < 0.85:
            return "Caution"
        return "Unsafe"

    raise ValueError(f"Unknown bacterium: {bacteria}")


def calculate_overall_risk(e_coli_risk, enterococcus_risk):
    return max(
        [e_coli_risk, enterococcus_risk],
        key=lambda value: RISK_RANK[value],
    )


def validate_prediction_row(row):
    row = pd.Series(row)

    errors = []
    warnings = []

    prediction_date = pd.to_datetime(
        row.get("prediction_date"),
        errors="coerce",
    )

    if pd.isna(prediction_date):
        errors.append("Prediction date is invalid.")
    else:
        if prediction_date.tzinfo is not None:
            prediction_date = prediction_date.tz_localize(None)

        prediction_date = prediction_date.normalize()
        today = pd.Timestamp.today().normalize()

        days_old = (today - prediction_date).days

        if days_old > 7:
            warnings.append(
                f"Prediction is {days_old} days old."
            )

    probabilities = {}

    for column in [
        "e_coli_probability",
        "enterococcus_probability",
    ]:
        value = pd.to_numeric(
            pd.Series([row.get(column)]),
            errors="coerce",
        ).iloc[0]

        if pd.isna(value):
            errors.append(
                f"{column} must be numeric."
            )
            continue

        value = float(value)

        if not 0 <= value <= 1:
            errors.append(
                f"{column} must be between 0 and 1."
            )

        probabilities[column] = value

    for column in [
        "e_coli_risk",
        "enterococcus_risk",
        "overall_risk",
    ]:
        risk = str(
            row.get(column, "")
        ).strip()

        if risk not in VALID_RISKS:
            errors.append(
                f"{column} must be Safe, Caution, or Unsafe."
            )

    ecoli_risk = str(
        row.get("e_coli_risk", "")
    ).strip()

    entero_risk = str(
        row.get("enterococcus_risk", "")
    ).strip()

    overall = str(
        row.get("overall_risk", "")
    ).strip()

    if (
        "e_coli_probability" in probabilities
        and ecoli_risk in VALID_RISKS
    ):
        expected = classify_risk(
            "E. coli",
            probabilities["e_coli_probability"],
        )

        if ecoli_risk != expected:
            errors.append(
                "E. coli probability does not match its risk label."
            )

    if (
        "enterococcus_probability" in probabilities
        and entero_risk in VALID_RISKS
    ):
        expected = classify_risk(
            "Enterococcus",
            probabilities["enterococcus_probability"],
        )

        if entero_risk != expected:
            errors.append(
                "Enterococcus probability does not match its risk label."
            )

    if (
        ecoli_risk in VALID_RISKS
        and entero_risk in VALID_RISKS
        and overall in VALID_RISKS
    ):
        expected_overall = calculate_overall_risk(
            ecoli_risk,
            entero_risk,
        )

        if overall != expected_overall:
            errors.append(
                "Overall risk does not match the more serious bacteria risk."
            )

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "stale": any(
            "days old" in warning
            for warning in warnings
        ),
    }


def validate_saved_csv(path=PREDICTION_CSV):
    status = {
        "loaded": False,
        "error": None,
        "missing_columns": [],
        "duplicate_count": 0,
        "invalid_rows": 0,
        "valid_rows": 0,
        "latest_prediction_date": None,
        "stale": False,
    }

    try:
        df = pd.read_csv(path)
        status["loaded"] = True

    except Exception as exc:
        status["error"] = str(exc)
        return pd.DataFrame(), status

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    status["missing_columns"] = missing

    if missing:
        return pd.DataFrame(), status

    df = df.copy()

    df["prediction_date"] = pd.to_datetime(
        df["prediction_date"],
        errors="coerce",
    )

    duplicate_mask = df.duplicated(
        subset=[
            "site_id",
            "prediction_date",
        ],
        keep=False,
    )

    status["duplicate_count"] = int(
        duplicate_mask.sum()
    )

    if status["duplicate_count"] > 0:
        return pd.DataFrame(), status

    valid_rows = []

    for _, row in df.iterrows():
        result = validate_prediction_row(row)

        if result["valid"]:
            valid_rows.append(row)
        else:
            status["invalid_rows"] += 1

    if not valid_rows:
        return pd.DataFrame(), status

    valid_df = (
        pd.DataFrame(valid_rows)
        .sort_values("prediction_date")
        .reset_index(drop=True)
    )

    status["valid_rows"] = len(valid_df)

    latest_date = valid_df[
        "prediction_date"
    ].max()

    status["latest_prediction_date"] = latest_date

    status["stale"] = (
        (
            pd.Timestamp.today().normalize()
            - latest_date.normalize()
        ).days
        > 7
    )

    return valid_df, status


def load_valid_latest():
    df, status = validate_saved_csv()

    if not status["loaded"]:
        raise RuntimeError(
            "Prediction CSV could not be loaded."
        )

    if status["missing_columns"]:
        raise RuntimeError(
            "Prediction CSV is missing required columns."
        )

    if status["duplicate_count"]:
        raise RuntimeError(
            "Duplicate prediction records detected."
        )

    if df.empty:
        raise RuntimeError(
            "No valid saved predictions are available."
        )

    return df.iloc[-1].copy()
