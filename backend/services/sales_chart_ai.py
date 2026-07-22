import pandas as pd
from difflib import get_close_matches

from services.gemini_service import GeminiService



class SalesChartAI:


    def __init__(self, df):

        self.df = df.copy()


    # ----------------------------
    # Convert numeric text columns
    # ----------------------------

    def convert_numeric_columns(self):

        for col in self.df.columns:


            if self.df[col].dtype == "object":

                cleaned = (
                    self.df[col]
                    .astype(str)
                    .str.replace(
                        r"[^\d\.\-]",
                        "",
                        regex=True
                    )
                    .replace(
                        "",
                        pd.NA
                    )
                )


                converted = pd.to_numeric(
                    cleaned,
                    errors="coerce"
                )


                # Convert only useful numeric columns

                if converted.notna().sum() > len(self.df)*0.3:

                    self.df[col] = converted



    # ----------------------------
    # Match Gemini columns
    # ----------------------------

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



    # ----------------------------
    # Remove ID columns
    # ----------------------------

    def remove_identifier_columns(self, cols):

        ignore = [

            "id",
            "product_id",
            "user_id",
            "review_id",
            "order_id",
            "customer_id",
            "img_link",
            "product_link"

        ]


        return [

            c for c in cols

            if c.lower() not in ignore

        ]



    # ----------------------------
    # Main function
    # ----------------------------

    def generate(self):


        # FIRST CLEAN DATA

        self.convert_numeric_columns()



        print(
            "Columns after conversion:"
        )

        print(
            self.df.dtypes
        )



        # Gemini recommendation

        chart = GeminiService().get_sales_chart(
            self.df
        )


        print("\n GEMINI RESPONSE")
        print(chart)



        x = self.closest_column(
            chart.get("xAxis")
        )


        y = self.closest_column(
            chart.get("yAxis")
        )



        print("\nMatched Columns")
        print("X =",x)
        print("Y =",y)



        # ----------------------------
        # Fallback logic
        # ----------------------------


        object_cols = (

            self.df
            .select_dtypes(include=["object"])
            .columns
            .tolist()

        )


        numeric_cols = (

            self.df
            .select_dtypes(include="number")
            .columns
            .tolist()

        )


        object_cols = self.remove_identifier_columns(
            object_cols
        )

        numeric_cols = self.remove_identifier_columns(
            numeric_cols
        )



        if x is None:

            if object_cols:

                x = object_cols[0]

            else:

                x = self.df.columns[0]



        if y is None or y not in numeric_cols:


            if numeric_cols:

                priority = [

                    "sales",
                    "revenue",
                    "amount",
                    "actual_price",
                    "discounted_price",
                    "profit",
                    "rating",
                    "quantity"

                ]


                y = next(
                    (
                        c for c in numeric_cols
                        if c.lower() in priority
                    ),
                    numeric_cols[0]
                )


            else:

                raise Exception(
                    "No numeric data found"
                )



        # Ensure numeric

        self.df[y] = pd.to_numeric(
            self.df[y],
            errors="coerce"
        )



        self.df = self.df.dropna(
            subset=[y]
        )



        if self.df.empty:

            raise Exception(
                f"No numeric data found in {y}"
            )



        aggregation = chart.get(
            "aggregation",
            "sum"
        )



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



        result = (
            result
            .sort_values(
                y,
                ascending=False
            )
            .head(10)
        )



        result[x] = result[x].astype(str)



        print("\nChart Data")
        print(result.head())



        return {


            "chartType": chart.get(
                "chartType",
                "bar"
            ),


            "title": chart.get(
                "title",
                "Business Analysis"
            ),


            "xAxis": x,


            "yAxis": y,


            "data":
                result.to_dict(
                    "records"
                )

        }