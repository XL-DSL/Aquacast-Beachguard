import unittest

import pandas as pd

from utils.validation import (
    calculate_overall_risk,
    classify_risk,
    validate_prediction_row,
)


def valid_row():
    return pd.Series(
        {
            "site_id": "parkside_aquatic_park_san_mateo",
            "site_name": "Parkside Aquatic Park, San Mateo",
            "prediction_date": pd.Timestamp.today(),
            "data_last_updated": pd.Timestamp.today(),
            "e_coli_probability": 0.05,
            "enterococcus_probability": 0.20,
            "e_coli_risk": "Safe",
            "enterococcus_risk": "Safe",
            "overall_risk": "Safe",
            "model_version": "TEST",
        }
    )


class RiskBoundaryTests(unittest.TestCase):

    def test_ecoli_010(self):
        self.assertEqual(
            classify_risk(
                "E. coli",
                0.10,
            ),
            "Caution",
        )

    def test_ecoli_050(self):
        self.assertEqual(
            classify_risk(
                "E. coli",
                0.50,
            ),
            "Unsafe",
        )

    def test_enterococcus_040(self):
        self.assertEqual(
            classify_risk(
                "Enterococcus",
                0.40,
            ),
            "Caution",
        )

    def test_enterococcus_085(self):
        self.assertEqual(
            classify_risk(
                "Enterococcus",
                0.85,
            ),
            "Unsafe",
        )

    def test_overall_safe_and_caution(self):
        self.assertEqual(
            calculate_overall_risk(
                "Safe",
                "Caution",
            ),
            "Caution",
        )

    def test_overall_unsafe_and_safe(self):
        self.assertEqual(
            calculate_overall_risk(
                "Unsafe",
                "Safe",
            ),
            "Unsafe",
        )

    def test_overall_caution_and_unsafe(self):
        self.assertEqual(
            calculate_overall_risk(
                "Caution",
                "Unsafe",
            ),
            "Unsafe",
        )


class ValidationTests(unittest.TestCase):

    def test_valid_prediction(self):
        row = valid_row()

        result = validate_prediction_row(
            row
        )

        self.assertTrue(
            result["valid"]
        )

    def test_negative_probability(self):
        row = valid_row()

        row[
            "e_coli_probability"
        ] = -0.01

        result = validate_prediction_row(
            row
        )

        self.assertFalse(
            result["valid"]
        )

    def test_probability_above_one(self):
        row = valid_row()

        row[
            "e_coli_probability"
        ] = 1.01

        result = validate_prediction_row(
            row
        )

        self.assertFalse(
            result["valid"]
        )

    def test_text_probability(self):
        row = valid_row()

        row[
            "e_coli_probability"
        ] = "high"

        result = validate_prediction_row(
            row
        )

        self.assertFalse(
            result["valid"]
        )

    def test_blank_probability(self):
        row = valid_row()

        row[
            "e_coli_probability"
        ] = ""

        result = validate_prediction_row(
            row
        )

        self.assertFalse(
            result["valid"]
        )

    def test_malformed_date(self):
        row = valid_row()

        row[
            "prediction_date"
        ] = "bad-date"

        result = validate_prediction_row(
            row
        )

        self.assertFalse(
            result["valid"]
        )

    def test_wrong_ecoli_risk_label(self):
        row = valid_row()

        row[
            "e_coli_probability"
        ] = 0.60

        row[
            "e_coli_risk"
        ] = "Safe"

        result = validate_prediction_row(
            row
        )

        self.assertFalse(
            result["valid"]
        )

    def test_wrong_enterococcus_risk_label(self):
        row = valid_row()

        row[
            "enterococcus_probability"
        ] = 0.90

        row[
            "enterococcus_risk"
        ] = "Safe"

        result = validate_prediction_row(
            row
        )

        self.assertFalse(
            result["valid"]
        )

    def test_wrong_overall_risk(self):
        row = valid_row()

        row[
            "e_coli_probability"
        ] = 0.70

        row[
            "e_coli_risk"
        ] = "Unsafe"

        row[
            "overall_risk"
        ] = "Safe"

        result = validate_prediction_row(
            row
        )

        self.assertFalse(
            result["valid"]
        )

    def test_stale_prediction_warning(self):
        row = valid_row()

        row[
            "prediction_date"
        ] = (
            pd.Timestamp.today()
            - pd.Timedelta(
                days=8
            )
        )

        result = validate_prediction_row(
            row
        )

        self.assertTrue(
            result["stale"]
        )

    def test_seven_days_is_not_stale(self):
        row = valid_row()

        row[
            "prediction_date"
        ] = (
            pd.Timestamp.today()
            - pd.Timedelta(
                days=7
            )
        )

        result = validate_prediction_row(
            row
        )

        self.assertFalse(
            result["stale"]
        )


if __name__ == "__main__":
    unittest.main()
