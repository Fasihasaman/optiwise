import pandas as pd
import numpy as np


class SalesChartAI:


    def __init__(self, df):

        self.df = df.copy()



    # -------------------------------
    # Convert numeric values
    # -------------------------------

    def convert_numbers(self):

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

                )


                converted = pd.to_numeric(
                    cleaned,
                    errors="coerce"
                )


                # if more than 50% values are numbers

                if converted.notna().mean() > 0.5:

                    self.df[col] = converted



    # -------------------------------
    # Remove IDs
    # -------------------------------

    def remove_ids(self, cols):


        ignore = [

            "id",
            "product_id",
            "customer_id",
            "customer id",
            "order_id",
            "order id",
            "user_id",
            "review_id",
            "postal_code",
            "img_link",
            "product_link"

        ]


        return [

            c for c in cols

            if c.lower() not in ignore

        ]




    # -------------------------------
    # Find numeric column
    # -------------------------------

    def get_numeric(self):


        cols = (

            self.df
            .select_dtypes(
                include=np.number
            )
            .columns
            .tolist()

        )


        cols=self.remove_ids(cols)


        priority=[

            "sales",
            "revenue",
            "profit",
            "amount",
            "price",
            "discounted_price",
            "actual_price",
            "quantity",
            "rating_count",
            "rating"

        ]


        for p in priority:

            for c in cols:

                if c.lower()==p:

                    return c



        if cols:

            return cols[0]


        return None




    # -------------------------------
    # Find category column
    # -------------------------------

    def get_category(self):


        cols=(

            self.df
            .select_dtypes(
                include="object"
            )
            .columns
            .tolist()

        )


        cols=self.remove_ids(cols)



        priority=[

            "category",
            "sub-category",
            "subcategory",
            "segment",
            "region",
            "state",
            "city",
            "product_name"

        ]


        for p in priority:

            for c in cols:

                if c.lower()==p:

                    return c



        if cols:

            return cols[0]


        return None




    # -------------------------------
    # Detect chart type
    # -------------------------------

    def detect_chart(self,x,y):


        unique_count=self.df[x].nunique()


        if pd.api.types.is_datetime64_any_dtype(
            self.df[x]
        ):

            return "line"



        if unique_count <= 10:

            return "pie"



        if unique_count <= 50:

            return "bar"



        return "bar"





    # -------------------------------
    # Generate Chart
    # -------------------------------

    def generate(self):


        self.convert_numbers()



        print("\nDATA TYPES")

        print(self.df.dtypes)



        x=self.get_category()

        y=self.get_numeric()



        if x is None:

            raise Exception(
                "No categorical column found"
            )


        if y is None:

            raise Exception(
                "No numeric column found"
            )



        print(
            "\nSELECTED"
        )

        print(
            "X:",
            x
        )

        print(
            "Y:",
            y
        )



        # clean numeric

        self.df[y]=pd.to_numeric(

            self.df[y],

            errors="coerce"

        )



        self.df=self.df.dropna(
            subset=[y]
        )



        # aggregation

        chart_type=self.detect_chart(
            x,
            y
        )



        result=(

            self.df
            .groupby(x)[y]
            .sum()
            .reset_index()

        )



        result=(

            result
            .sort_values(
                y,
                ascending=False
            )
            .head(10)

        )



        result[x]=result[x].astype(str)



        print(
            "\nCHART RESULT"
        )

        print(result)



        return {


            "chartType":
                chart_type,


            "title":
                f"{y} by {x}",


            "xAxis":
                x,


            "yAxis":
                y,


            "data":
                result.to_dict(
                    "records"
                )

        }