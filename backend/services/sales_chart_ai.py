import pandas as pd
from difflib import get_close_matches

from services.gemini_service import GeminiService


class SalesChartAI:


    def __init__(self, df):

        self.df = df.copy()



    # -------------------------------
    # Convert text numbers to numeric
    # -------------------------------

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
                )


                converted = pd.to_numeric(
                    cleaned,
                    errors="coerce"
                )


                valid_ratio = (
                    converted.notna().sum()
                    /
                    len(self.df)
                )


                # Convert only meaningful numeric columns

                if valid_ratio > 0.3:

                    self.df[col] = converted



    # -------------------------------
    # Find closest column name
    # -------------------------------

    def closest_column(self, name):

        if not name:
            return None


        columns = list(
            self.df.columns
        )


        if name in columns:

            return name


        matches = get_close_matches(

            name,

            columns,

            n=1,

            cutoff=0.5
        )


        return matches[0] if matches else None



    # -------------------------------
    # Remove unwanted columns
    # -------------------------------

    def remove_bad_columns(self, columns):

        ignore = [

            "id",
            "row id",
            "row_id",
            "order id",
            "order_id",
            "customer id",
            "customer_id",
            "product id",
            "product_id",
            "user id",
            "user_id",
            "review id",
            "review_id",
            "postal code",
            "postal_code",
            "zip",
            "img_link",
            "product_link"

        ]


        result = []


        for col in columns:

            if col.lower() not in ignore:

                result.append(col)


        return result



    # -------------------------------
    # Select best numeric column
    # -------------------------------

    def select_numeric_column(self, numeric_cols):

        priority = [

            "sales",
            "revenue",
            "amount",
            "price",
            "actual_price",
            "discounted_price",
            "profit",
            "rating_count",
            "rating",
            "quantity"

        ]


        for p in priority:

            for col in numeric_cols:

                if col.lower() == p:

                    return col



        return numeric_cols[0]



    # -------------------------------
    # Main chart generator
    # -------------------------------

    def generate(self):


        # Step 1
        # Convert numeric text

        self.convert_numeric_columns()



        print("\nCOLUMN TYPES")

        print(
            self.df.dtypes
        )



        # Step 2
        # Gemini recommendation


        chart = GeminiService().get_sales_chart(
            self.df
        )


        print(
            "\nGEMINI RESPONSE"
        )

        print(chart)



        # Step 3
        # Match columns


        x = self.closest_column(
            chart.get("xAxis")
        )


        y = self.closest_column(
            chart.get("yAxis")
        )



        # Step 4
        # Validate y-axis


        numeric_columns = (

            self.df
            .select_dtypes(
                include="number"
            )
            .columns
            .tolist()

        )


        numeric_columns = self.remove_bad_columns(
            numeric_columns
        )



        if y not in numeric_columns:

            y = self.select_numeric_column(
                numeric_columns
            )



        # Step 5
        # Validate x-axis


        object_columns = (

            self.df
            .select_dtypes(
                include="object"
            )
            .columns
            .tolist()

        )


        object_columns = self.remove_bad_columns(
            object_columns
        )


        if x not in object_columns:


            if object_columns:

                x = object_columns[0]

            else:

                x = self.df.columns[0]



        print("\nFINAL COLUMNS")

        print(
            "X =",
            x
        )

        print(
            "Y =",
            y
        )



        # Step 6
        # Clean numeric data


        self.df[y] = pd.to_numeric(

            self.df[y],

            errors="coerce"

        )


        self.df = self.df.dropna(
            subset=[y]
        )



        if self.df.empty:

            raise Exception(
                "No valid numeric data found"
            )



        # Step 7
        # Aggregation


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



        # Top 10 values

        result = (

            result
            .sort_values(
                y,
                ascending=False
            )
            .head(10)

        )


        result[x] = (

            result[x]
            .astype(str)

        )



        print(
            "\nCHART DATA"
        )

        print(result)



        return {


            "chartType":
                chart.get(
                    "chartType",
                    "bar"
                ),


            "title":
                chart.get(
                    "title",
                    "Business Analysis"
                ),


            "xAxis":
                x,


            "yAxis":
                y,


            "data":
                result.to_dict(
                    "records"
                )

        }