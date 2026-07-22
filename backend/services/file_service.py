import pandas as pd
import numpy as np
import os
from utils.analyzer import analyze_data
from utils.recommender import generate_recommendations
from services.ai_service import ask_ai
from services.chart_service import generate_charts

def process_file(filepath):

   
    # READ FILE
   

    try:

        if filepath.endswith(".csv"):

            try:
                df = pd.read_csv(
                    filepath,
                    encoding="utf-8"
                )

            except:
                df = pd.read_csv(
                    filepath,
                    encoding="latin1"
                )

        elif filepath.endswith(".xlsx"):

            df = pd.read_excel(
                filepath,
                engine="openpyxl"
            )

        elif filepath.endswith(".xls"):

            df = pd.read_excel(
                filepath,
                engine="xlrd"
            )

        else:

            raise Exception(
                "Unsupported file format"
            )

    except Exception as e:

        raise Exception(
            f"File reading error: {str(e)}"
        )

   
    # BASIC INFO
   

    rows = int(df.shape[0])
    cols = int(df.shape[1])

    column_names = list(df.columns)




# DATASET METRICS


    missing_values = int(df.isnull().sum().sum())

    memory_usage = round(
    df.memory_usage(deep=True).sum() / (1024 * 1024),
    2
    )
    

   
    # ANALYSIS
   

    analysis = analyze_data(df)

    recommendations = generate_recommendations(df)

    
       
      
       # AI SALES CHART
      

    chart_response = generate_charts(df)

    recommended_charts = chart_response["salesChart"]

    forecast_chart = None

    column_info = {}
   
    # KPI SECTION
   

    total_sales = 0
    total_profit = 0
    total_quantity = 0

    if "Sales" in df.columns:

        total_sales = float(
            round(
                df["Sales"].sum(),
                2
            )
        )

    if "Profit" in df.columns:

        total_profit = float(
            round(
                df["Profit"].sum(),
                2
            )
        )

    if "Quantity" in df.columns:

        total_quantity = float(
            round(
                df["Quantity"].sum(),
                2
            )
        )

   
    # AI SUMMARY
   

    try:

        preview = (
            df.head(5)
            .to_string()
        )

        prompt = f"""
Analyze this business dataset professionally.

Rows: {rows}
Columns: {cols}

Columns:
{column_names}

Preview:
{preview}

Generate:

1. Executive Summary
2. Business Insights
3. Risks
4. Opportunities
5. Recommendations
"""

        summary = ask_ai(
            question="summary",
            direct_prompt=prompt
        )

    except Exception as e:

        print(
            "AI SUMMARY ERROR:",
            e
        )

        summary = f"""
Dataset contains {rows} rows and {cols} columns.

The dataset has been successfully processed and is ready for analytics.
"""


# DATASET NAME


    dataset_name = os.path.basename(filepath)
   
    # FINAL RESPONSE
   

    result = {

        "dataset_name": dataset_name,
        "rows": rows,

        "columns": cols,

        "column_names": column_names,
        

        

        "column_info": column_info,

        "insights":
            analysis.get(
                "insights",
                []
            ),

        "predictions":
            analysis.get(
                "predictions",
                []
            ),

        "feature_importance":
            analysis.get(
                "feature_importance",
                []
            ),

        "shap_data":
            analysis.get(
                "shap_data",
                []
            ),

        "xai_explanation":
            analysis.get(
                "xai_explanation",
                ""
            ),

        "recommendations":
            recommendations,

        "recommended_charts": recommended_charts,

        "forecast_chart":
            forecast_chart,

        "summary":
            summary,

        "kpis": {

         "total_sales": total_sales,

         "total_profit": total_profit,

         "total_quantity": total_quantity,

        

          

         "missing_values": missing_values,

         "memory_usage": memory_usage




        }
        

    }
    print("RECOMMENDED CHARTS")
    print(recommended_charts)

    

    return result, df