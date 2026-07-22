
# FEATURE IMPORTANCE


def generate_feature_importance(model, X):

    try:

        importance = model.feature_importances_

        feature_data = []

        for feature, value in zip(
            X.columns,
            importance
        ):

            feature_data.append({

                "feature": feature,

                "importance": round(
                    float(value),
                    4
                )
            })

        feature_data = sorted(

            feature_data,

            key=lambda x: x["importance"],

            reverse=True
        )

        return feature_data

    except Exception as e:

        print(
            "FEATURE IMPORTANCE ERROR:",
            e
        )

        return []



# XAI FEATURE IMPACT


def generate_shap_explanations(model, X):

    try:

        importance = model.feature_importances_

        impact_data = []

        for feature, value in zip(
            X.columns,
            importance
        ):

            impact_data.append({

                "feature": feature,

                "impact": round(
                    float(value),
                    4
                )
            })

        impact_data = sorted(

            impact_data,

            key=lambda x: x["impact"],

            reverse=True
        )

        return impact_data

    except Exception as e:

        print(
            "IMPACT ERROR:",
            e
        )

        return []



# BUSINESS EXPLANATION


def generate_business_explanation(
    feature_importance
):

    try:

        if not feature_importance:

            return (
                "No Explainable AI insights could be generated."
            )

        top_feature = feature_importance[0]

        top_three = feature_importance[:3]

        explanation = f"""
The AI model identified '{top_feature['feature']}'
as the most influential feature affecting predictions.

Top factors influencing business outcomes:

"""

        for item in top_three:

            explanation += (
                f"- {item['feature']} "
                f"(Importance: {item['importance']})\n"
            )

        explanation += """

These features contribute most strongly to the model's decision-making process and should be prioritized for business optimization and strategic planning.
"""

        return explanation

    except Exception as e:

        print(
            "EXPLANATION ERROR:",
            e
        )

        return "Explanation generation failed."