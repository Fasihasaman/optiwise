from flask import Blueprint, jsonify
from utils.model import train_model
import services.data_store as store

predict_bp = Blueprint("predict_bp", __name__)


@predict_bp.route("/predict")
def predict():

    try:

        # Check dataset uploaded
        if store.data_store is None:

            return jsonify({
                "prediction": "Please upload dataset first"
            })

        # Train ML model
        result = train_model(store.data_store)

        return jsonify({
            "prediction": result
        })

    except Exception as e:

        return jsonify({
            "prediction": str(e)
        }), 500