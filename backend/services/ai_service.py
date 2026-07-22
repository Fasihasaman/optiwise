from google import genai
import pandas as pd
import services.data_store as store

from dotenv import load_dotenv
import os


# LOAD ENV VARIABLES


load_dotenv()


# GEMINI CLIENT


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# AI GENERATOR


def generate_ai(prompt):

    response = client.models.generate_content(

        model="gemini-2.5-flash-lite",

        contents=prompt
    )

    return response.text


# MAIN AI FUNCTION


def ask_ai(question=None, direct_prompt=None):

    try:

       
        # DIRECT PROMPT MODE
       

        if direct_prompt:

            return generate_ai(direct_prompt)

       
        # GET DATASET
       

        df = store.data_store

        if df is None:

            return "Please upload dataset first."

       
        # BASIC INFO
       

        question = question.lower()

        numeric_df = df.select_dtypes(
            include=["number"]
        )

        rows = int(df.shape[0])

        cols = int(df.shape[1])

        columns = ", ".join(df.columns)

        preview = df.head(5).to_string()

       
        # TOTAL ANALYSIS
       

        if "total" in question or "sum" in question:

            totals = numeric_df.sum()

            result = totals.to_string()

            prompt = f"""

            You are a professional business analyst.

            Dataset Totals:
            {result}

            Explain:
            - Business meaning
            - KPIs
            - Financial interpretation
            - Operational insights
            - Strategic recommendations

            """

            ai_text = generate_ai(prompt)

            return f"""

TOTAL ANALYSIS

{result}

AI INSIGHTS:
{ai_text}

"""

       
        # AVERAGE ANALYSIS
       

        elif "average" in question or "mean" in question:

            averages = numeric_df.mean()

            result = averages.to_string()

            prompt = f"""

            Dataset Averages:
            {result}

            Explain:
            - Trends
            - Business impact
            - Operational meaning
            - Recommendations

            """

            ai_text = generate_ai(prompt)

            return f"""

AVERAGE ANALYSIS

{result}

AI INSIGHTS:
{ai_text}

"""

       
        # MAX ANALYSIS
       

        elif (
            "highest" in question
            or "maximum" in question
            or "max" in question
        ):

            maximums = numeric_df.max()

            result = maximums.to_string()

            prompt = f"""

            Maximum values:
            {result}

            Explain:
            - Business significance
            - Opportunities
            - Risks
            - Important insights

            """

            ai_text = generate_ai(prompt)

            return f"""

MAXIMUM VALUE ANALYSIS

{result}

AI INSIGHTS:
{ai_text}

"""

       
        # MIN ANALYSIS
       

        elif (
            "minimum" in question
            or "lowest" in question
            or "min" in question
        ):

            minimums = numeric_df.min()

            result = minimums.to_string()

            prompt = f"""

            Minimum values:
            {result}

            Explain:
            - Weaknesses
            - Risks
            - Concerns
            - Recommendations

            """

            ai_text = generate_ai(prompt)

            return f"""

MINIMUM VALUE ANALYSIS

{result}

AI INSIGHTS:
{ai_text}

"""

       
        # MISSING VALUES
       

        elif (
            "missing" in question
            or "null" in question
        ):

            missing = df.isnull().sum()

            result = missing.to_string()

            prompt = f"""

            Missing values report:
            {result}

            Explain:
            - Data quality issues
            - Cleaning recommendations
            - Risks for ML models

            """

            ai_text = generate_ai(prompt)

            return f"""

MISSING VALUE ANALYSIS

{result}

AI INSIGHTS:
{ai_text}

"""

       
        # SUMMARY ANALYSIS
       

        elif (
            "summary" in question
            or "overview" in question
        ):

            describe = numeric_df.describe().to_string()

            prompt = f"""

            Dataset Summary:
            {describe}

            Explain:
            - Key patterns
            - Important insights
            - Risks
            - Opportunities
            - Strategic recommendations

            """

            ai_text = generate_ai(prompt)

            return f"""

DATASET SUMMARY

Rows: {rows}
Columns: {cols}

Dataset Columns:
{columns}

Statistical Summary:
{describe}

AI INSIGHTS:
{ai_text}

"""

       
        # CORRELATION ANALYSIS
       

        elif (
            "correlation" in question
            or "relationship" in question
        ):

            correlation = numeric_df.corr().to_string()

            prompt = f"""

            Correlation Matrix:
            {correlation}

            Explain:
            - Strong relationships
            - Business trends
            - Predictive insights
            - Important observations

            """

            ai_text = generate_ai(prompt)

            return f"""

CORRELATION ANALYSIS

{correlation}

AI INSIGHTS:
{ai_text}

"""

       
        # DEFAULT AI ANALYSIS
       

        else:

            prompt = f"""

            You are an advanced AI Decision Intelligence System.

            Dataset Information:
            Rows: {rows}
            Columns: {cols}

            Dataset Columns:
            {columns}

            Dataset Sample:
            {preview}

            User Question:
            {question}

            Provide:
            - Business analysis
            - Intelligent insights
            - Trend analysis
            - Risk analysis
            - Opportunities
            - Recommendations
            - Predictive observations

            Keep response professional,
            concise,
            and actionable.

            """

            return generate_ai(prompt)

    except Exception as e:

        return f"AI Error: {str(e)}"