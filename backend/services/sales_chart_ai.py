import pandas as pd
from difflib import get_close_matches

from services.gemini_service import GeminiService


class SalesChartAI:


    def __init__(self, df):

        self.df = df.copy()



    # -----------------------------------
    # Convert numeric text columns
    # -----------------------------------

    def convert_numeric_columns(self):

        for col in self.df.columns:


            if self.df[col].dtype == "object":


                cleaned = (

                    self.df[col]
                    .astype(str)

                    .str.replace(
                        ",",
                        "",
                        regex=False
                    )

                    .str.replace(
                        "₹",
                        "",
                        regex=False
                    )

                    .str.replace(
                        "%",
                        "",
                        regex=False
                    )

                    .str.strip()

                )


                converted = pd.to_numeric(

                    cleaned,

                    errors="coerce"

                )


                numeric_count = converted.notna().sum()


                if numeric_count > 0:

                    self.df[col] = converted



    # -----------------------------------
    # Match Gemini column names
    # -----------------------------------

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


        if matches:

            return matches[0]


        return None



    # -----------------------------------
    # Remove unwanted columns
    # -----------------------------------

    def remove_bad_columns(self, columns):


        unwanted = [

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

            "img_link",
            "product_link"

        ]


        result = []


        for col in columns:


            if col.lower() not in unwanted:

                result.append(col)


        return result



    # -----------------------------------
    # Select best numeric column
    # -----------------------------------

    def select_best_numeric(self, columns):


        priority = [

            "sales",

            "revenue",

            "amount",

            "profit",

            "actual_price",

            "discounted_price",

            "price",

            "rating_count",

            "rating",

            "quantity"

        ]



        for item in priority:


            for col in columns:


                if col.lower() == item:

                    return col



        return columns[0]



    # -----------------------------------
    # Select best category column
    # -----------------------------------

    def select_best_category(self, columns):


        priority = [

            "category",

            "sub-category",

            "subcategory",

            "segment",

            "region",

            "state",

            "city",

            "product_name"

        ]



        for item in priority:


            for col in columns:


                if col.lower() == item:

                    return col



        return columns[0]



    # -----------------------------------
    # Main chart generator
    # -----------------------------------

    def generate(self):


        # Step 1:
        # Convert text numbers

        self.convert_numeric_columns()



        print("\nColumns After Conversion")

        print(
            self.df.dtypes
        )



        # Step 2:
        # Gemini recommendation


        chart = GeminiService().get_sales_chart(

            self.df

        )



        print(
            "\nGEMINI RESPONSE"
        )

        print(chart)



        # Step 3:
        # Extract columns


        x = self.closest_column(

            chart.get("xAxis")

        )


        y = self.closest_column(

            chart.get("yAxis")

        )



        # Step 4:
        # Get available columns


        numeric_columns = (

            self.df
            .select_dtypes(
                include="number"
            )
            .columns
            .tolist()

        )


        object_columns = (

            self.df
            .select_dtypes(
                include="object"
            )
            .columns
            .tolist()

        )



        numeric_columns = self.remove_bad_columns(

            numeric_columns

        )


        object_columns = self.remove_bad_columns(

            object_columns

        )



        # Step 5:
        # Validate y-axis


        invalid_y = [

            "product_id",

            "user_id",

            "review_id",

            "product_link",

            "img_link",

            "order_id"

        ]



        if y and y.lower() in invalid_y:

            y = None



        if y not in numeric_columns:


            if numeric_columns:

                y = self.select_best_numeric(

                    numeric_columns

                )

            else:

                raise Exception(

                    "No numeric data found"

                )



        # Step 6:
        # Validate x-axis


        if x not in object_columns:


            if object_columns:

                x = self.select_best_category(

                    object_columns

                )

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



        # Step 7:
        # Clean y column


        self.df[y] = pd.to_numeric(

            self.df[y],

            errors="coerce"

        )


        self.df = self.df.dropna(

            subset=[y]

        )



        if self.df.empty:

            raise Exception(

                "No valid numeric data after cleaning"

            )



        # Step 8:
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



        # Top 10

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



        print("\nChart Data")

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