from utils.model import train_model

from utils.xai_explainer import (
    generate_feature_importance,
    generate_shap_explanations,
    generate_business_explanation
)


def analyze_data(df):

    try:

        insights = [

            {
                "title": "Rows",
                "value": int(df.shape[0])
            },

            {
                "title": "Columns",
                "value": int(df.shape[1])
            },

            {
                "title": "Missing Values",
                "value": int(df.isnull().sum().sum())
            }

        ]

        feature_importance = []
        shap_data = []
        xai_explanation = ""
        predictions = []

        model_data = train_model(df)

        if model_data:

            model = model_data["model"]

            X = model_data["X"]

            predictions = model_data["predictions"]

            try:

                feature_importance = (
                    generate_feature_importance(
                        model,
                        X
                    )
                )

            except Exception as e:

                print(
                    "FEATURE IMPORTANCE ERROR:",
                    e
                )

            try:

                shap_data = (
                    generate_shap_explanations(
                        model,
                        X
                    )
                )

            except Exception as e:

                print(
                    "SHAP ERROR:",
                    e
                )

            try:

                xai_explanation = (
                    generate_business_explanation(
                        feature_importance
                    )
                )

            except Exception as e:

                print(
                    "XAI EXPLANATION ERROR:",
                    e
                )

        return {

            "insights": insights,

            "predictions": predictions,

            "feature_importance":
                feature_importance,

            "shap_data":
                shap_data,

            "xai_explanation":
                xai_explanation
        }

    except Exception as e:

        print("ANALYZER ERROR:", e)

        return {

            "insights": [],

            "predictions": [],

            "feature_importance": [],

            "shap_data": [],

            "xai_explanation": ""
        }