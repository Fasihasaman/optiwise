from flask import Blueprint, request, jsonify

from services.file_service import process_file

import services.data_store as store

import os
import traceback


upload_bp = Blueprint(
    "upload_bp",
    __name__
)

UPLOAD_FOLDER = "uploads"


# CREATE UPLOAD FOLDER


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

        print("\n")
        print("Saved file:", filepath)
        print("\n")

        
        # PROCESS FILE
        

        result, df = process_file(
            filepath
        )

        print("\n")
        print("Dataset Processed Successfully")
        print("Rows:", len(df))
        print("Columns:", len(df.columns))
        print("\n")

        
        # STORE DATA
        

        store.data_store = df
        store.file_path = filepath

        
        # RETURN RESULT
        

        return jsonify(result)

    except Exception as e:

        print("\n UPLOAD ERROR ")

        traceback.print_exc()

        print("Error Message:", str(e))

        print("\n")

        return jsonify({
            "error": str(e)
        }), 500