from flask import Blueprint, request, jsonify
from services.ai_service import ask_ai
import services.data_store as store
import pandas as pd

ask_bp = Blueprint("ask_bp", __name__)


@ask_bp.route("/ask", methods=["POST"])
def ask():

    try:

        # Reload dataset if needed
        if store.data_store is None:

            if store.file_path:

                if store.file_path.endswith(".csv"):

                    try:
                        store.data_store = pd.read_csv(
                            store.file_path,
                            encoding="utf-8"
                        )

                    except:
                        store.data_store = pd.read_csv(
                            store.file_path,
                            encoding="latin1"
                        )

                else:

                    store.data_store = pd.read_excel(
                        store.file_path
                    )

            else:

                return jsonify({
                    "answer": "Please upload dataset first."
                })

        data = request.get_json()

        question = data.get("question")

        if not question:

            return jsonify({
                "answer": "Question required."
            })

        # Ask Gemini AI
        answer = ask_ai(question)

        return jsonify({
            "answer": answer
        })

    except Exception as e:

        return jsonify({
            "answer": str(e)
        }), 500