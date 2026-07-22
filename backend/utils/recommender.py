def generate_recommendations(df):

    recommendations = []

  
    # FEATURE COUNT
  

    if df.shape[1] > 10:

        recommendations.append(
            "Dataset contains many features. Consider feature selection for optimized ML performance."
        )

  
    # MISSING VALUES
  

    if df.isnull().sum().sum() > 0:

        recommendations.append(
            "Dataset contains missing values. Data cleaning is recommended before prediction."
        )

  
    # DATA QUALITY
  

    if len(recommendations) == 0:

        recommendations.append(
            "Dataset quality looks good for analytics and machine learning."
        )

    return recommendations