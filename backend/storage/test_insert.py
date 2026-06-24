# backend/storage/test_insert.py

from backend.storage.repository import (
    save_analysis_run
)

analysis_id = save_analysis_run({

    "dataset_name":
        "lendingclub.csv",

    "dataset_type":
        "credit_risk",

    "confidence":
        100,

    "total_loans":
        2000,

    "chargeoff_rate":
        14.7,

    "top_risk_grade":
        "E"

})

print(
    f"Inserted Analysis ID: {analysis_id}"
)