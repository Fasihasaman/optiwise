from flask import Blueprint, request, jsonify
from services.file_service import process_file
import services.data_store as store
import os
import traceback
import numpy as np

upload_bp = Blueprint(
    "upload_bp",
    __name__
)

UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


@upload_bp.route(
    "/upload",
    methods=["POST"]
)
def upload():

    try:

        # CHECK FILE EXISTS

        if "file" not in request.files:

            return jsonify({
                "error": "No file uploaded"
            }), 400

        file = request.files["file"]

        if file.filename == "":

            return jsonify({
                "error": "No selected file"
            }), 400

        # SAVE FILE

        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(filepath)

        print("\nSaved file:", filepath)

        # PROCESS FILE

        result, df = process_file(filepath)

        print("Dataset Processed Successfully")
        print("Rows:", len(df))
        print("Columns:", len(df.columns))

        # STORE DATA

        store.data_store = df
        store.file_path = filepath

        # -----------------------------
        # DATASET EXPLORER DATA
        # -----------------------------

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

                "std": round(float(df[col].std()), 2)

            }

        result["datasetExplorer"] = {

            "dataset_name": os.path.basename(filepath),

            "columns": list(df.columns),

            "sample": sample,

            "statistics": statistics

        }

        return jsonify(result)

    except Exception as e:

        print("\nUPLOAD ERROR")

        traceback.print_exc()

        return jsonify({
            "error": str(e)
        }), 500