import re
import pandas as pd
from difflib import get_close_matches

from services.gemini_service import GeminiService


class SalesChartAI:

    def __init__(self, df):
        self.df = df.copy()

   
    # Match Gemini column with actual dataframe column
   

    def closest_column(self, name):

        cols = list(self.df.columns)

        if name in cols:
            return name

        matches = get_close_matches(
            name,
            cols,
            n=1,
            cutoff=0.5
        )

        if matches:
            return matches[0]

        return None

   
    # Convert any numeric-looking text into numbers
   

    def clean_numeric(self, series):

        return pd.to_numeric(

            series.astype(str)

            .str.replace(r"[^\d\.\-]", "", regex=True)

            .replace("", pd.NA),

            errors="coerce"
        )

   
    # Main Function
   

    def generate(self):

        # Ask Gemini
        chart = GeminiService().get_sales_chart(self.df)

        print("\n GEMINI RESPONSE ")
        print(chart)

        # Match columns
        x = self.closest_column(chart["xAxis"])
        y = self.closest_column(chart["yAxis"])

        print("\nMatched Columns")
        print("X =", x)
        print("Y =", y)

# -------------------------------
# FALLBACK IF GEMINI FAILS
# -------------------------------

        if x is None:

    # Prefer a categorical column
          object_cols = self.df.select_dtypes(include=["object"]).columns.tolist()

        if object_cols:
         x = object_cols[0]
        else:
         x = self.df.columns[0]

        if y is None:

         numeric_cols = self.df.select_dtypes(include="number").columns.tolist()
 
        if numeric_cols:
         y = numeric_cols[0]
        else:
         raise Exception("No numeric column found in dataset.")

        # Convert numeric column
        self.df[y] = self.clean_numeric(self.df[y])

        print("\nNumeric Preview")
        print(self.df[y].head())

        # Remove invalid values
        self.df = self.df.dropna(subset=[y])

        print("\nRemaining Rows:", len(self.df))

        if self.df.empty:
            raise Exception(
                f"No numeric data found in '{y}' after cleaning."
            )

        aggregation = chart.get(
            "aggregation",
            "sum"
        ).lower()

        # Aggregate
        if aggregation == "mean":

            result = (
                self.df
                .groupby(x)[y]
                .mean()
                .reset_index()
            )

        elif aggregation == "count":

            result = (
                self.df
                .groupby(x)[y]
                .count()
                .reset_index()
            )

        else:

            result = (
                self.df
                .groupby(x)[y]
                .sum()
                .reset_index()
            )

        # Sort for better visualization
        result = (
            result
            .sort_values(y, ascending=False)
            .head(10)
        )
        result[x] = result[x].astype(str).apply(
        lambda v: v.split("|")[-1] if "|" in v else v
         )

        print("\nChart Data")
        print(result.head())

        return {

            "chartType": chart.get(
                "chartType",
                "bar"
            ),

            "title": chart.get(
                "title",
                "Sales Analysis"
            ),

            "xAxis": x,

            "yAxis": y,

            "data": result.to_dict("records")
        }