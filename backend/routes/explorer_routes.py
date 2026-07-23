from flask import Blueprint, jsonify
import services.data_store as store
import numpy as np
import os
import pandas as pd

explorer_bp = Blueprint("explorer_bp", __name__)


@explorer_bp.route("/dataset-explorer", methods=["GET"])
def dataset_explorer():

  

    if not store.file_path or not os.path.exists(store.file_path):
        return jsonify({"error": "No dataset uploaded"}), 400

    if store.file_path.endswith(".csv"):
        df = pd.read_csv(store.file_path)
    else:
        df = pd.read_excel(store.file_path)

    # Dataset name
    dataset_name = (
        os.path.basename(store.file_path)
        if store.file_path
        else "Unknown Dataset"
    )

    sample = (
        df.head(100)
        .replace([np.inf, -np.inf], np.nan)
        .fillna("")
        .to_dict(orient="records")
    )

    statistics = {}

    numeric_cols = df.select_dtypes(include=np.number).columns

    for col in numeric_cols:

        statistics[col] = {
            "mean": round(float(df[col].mean()), 2),
            "median": round(float(df[col].median()), 2),
            "min": round(float(df[col].min()), 2),
            "max": round(float(df[col].max()), 2),
            "std": round(float(df[col].std()), 2),
        }

    return jsonify({

        "dataset_name": dataset_name,

        "columns": list(df.columns),

        "sample": sample,

        "statistics": statistics

    })