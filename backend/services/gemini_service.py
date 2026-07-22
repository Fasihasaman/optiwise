import os
import json
from google.genai.errors import ClientError
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class GeminiService:

    def get_sales_chart(self, df):

        columns = list(df.columns)

        summary = {
            "rows": len(df),
            "columns": columns,
            "sample": df.head(5).to_dict("records")
        }

        prompt = f"""
You are an expert Business Intelligence analyst.

Your task is to recommend the BEST sales visualization for this dataset.

IMPORTANT RULES

1. Use ONLY the column names listed below.
2. NEVER rename or invent column names.
3. xAxis and yAxis MUST exactly match one of the available columns.
4. Return ONLY valid JSON.
5. Prefer charts that provide meaningful business insights.

CHART SELECTION RULES

• If a date column exists, use it on the x-axis with the sales column on the y-axis and choose a line chart.
• Otherwise, use the best categorical column on the x-axis and a numeric sales-related column on the y-axis.
• Prefer detailed categorical columns over generic ones.

Priority for x-axis:
1. Sub-Category
2. Product Name
3. Product
4. Product Category
5. Segment
6. Region
7. State
8. Category (only if nothing better exists)

Priority for y-axis:
1. Sales
2. Revenue
3. Amount
4. Profit
5. Discounted Price
6. Price
7. Quantity

Aggregation:
• Sales/Revenue/Amount/Price -> sum
• Quantity -> sum
• Profit -> sum

Available Columns:
{columns}

Dataset Information:
Rows: {summary["rows"]}

Sample Data:
{summary["sample"]}

Return ONLY this JSON:

{{
    "chartType":"bar",
    "title":"Sales by Sub-Category",
    "xAxis":"",
    "yAxis":"",
    "aggregation":"sum"
}}
"""

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            text = response.text.strip()
            text = text.replace("```json", "").replace("```", "")

            return json.loads(text)

        except Exception as e:

            print("Gemini Chart Error:", e)

            print("USING LOCAL FALLBACK")

    
   

    
            object_cols = df.select_dtypes(include=["object"]).columns.tolist()
            numeric_cols = df.select_dtypes(include="number").columns.tolist()
            print("Object Columns:", object_cols)
            print("Numeric Columns:", numeric_cols)

            return {
             "chartType": "bar",
             "title": "Sales Analysis",
             "xAxis": object_cols[0] if object_cols else df.columns[0],
             "yAxis": numeric_cols[0] if numeric_cols else df.columns[-1],
             "aggregation": "sum"
              }