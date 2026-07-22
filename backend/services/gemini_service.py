import os
import json
import pandas as pd

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)



class GeminiService:


    def get_sales_chart(self, df):


        columns = list(df.columns)


        prompt = f"""

You are a Business Intelligence analyst.

Recommend the best visualization for this dataset.

Rules:

1. Use only existing column names.
2. xAxis must be categorical.
3. yAxis must be numeric.
4. Do not select ID columns.
5. Do not select URL columns.
6. Return only JSON.

Available columns:

{columns}


Return format:

{{
"chartType":"bar",
"title":"Business Analysis",
"xAxis":"",
"yAxis":"",
"aggregation":"sum"
}}

"""


        try:


            response = client.models.generate_content(

                model="gemini-2.0-flash",

                contents=prompt

            )


            text = response.text.strip()


            text = (
                text
                .replace(
                    "```json",
                    ""
                )
                .replace(
                    "```",
                    ""
                )
            )


            return json.loads(text)



        except Exception as e:


            print(
                "Gemini Chart Error:",
                e
            )


            print(
                "USING LOCAL FALLBACK"
            )


            return self.local_chart(df)





    # --------------------------------
    # Local chart recommendation
    # --------------------------------

    def local_chart(self, df):


        df = df.copy()



        # Convert numeric text columns

        for col in df.columns:


            if df[col].dtype == "object":


                cleaned = (

                    df[col]
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

                    .str.extract(
                        r"([-+]?\d*\.?\d+)"
                    )[0]

                )


                converted = pd.to_numeric(

                    cleaned,

                    errors="coerce"

                )


                if converted.notna().sum() > 5:

                    df[col] = converted





        # Find numeric columns


        numeric_cols = (

            df
            .select_dtypes(
                include="number"
            )
            .columns
            .tolist()

        )



        # Remove unwanted numeric columns


        ignore_numeric = [

            "id",
            "row id",
            "row_id",
            "postal code",
            "postal_code"

        ]



        numeric_cols = [

            c for c in numeric_cols

            if c.lower()
            not in ignore_numeric

        ]





        # Find categorical columns


        object_cols = (

            df
            .select_dtypes(
                include="object"
            )
            .columns
            .tolist()

        )



        ignore_object = [

            "product_id",
            "customer_id",
            "user_id",
            "review_id",
            "order_id",
            "product_link",
            "img_link"

        ]



        object_cols = [

            c for c in object_cols

            if c.lower()
            not in ignore_object

        ]





        # Select X column


        if "category" in df.columns:

            x = "category"


        elif object_cols:

            x = object_cols[0]


        else:

            x = df.columns[0]





        # Select Y column


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



        y = None



        for p in priority:


            for col in numeric_cols:


                if col.lower() == p:

                    y = col

                    break



            if y:

                break



        if y is None:


            if numeric_cols:

                y = numeric_cols[0]


            else:

                raise Exception(
                    "No numeric column available"
                )





        print(
            "LOCAL CHART:",
            x,
            y
        )



        return {


            "chartType":"bar",


            "title":
                f"{y} Analysis",


            "xAxis":x,


            "yAxis":y,


            "aggregation":"sum"

        }