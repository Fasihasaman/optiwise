from services.sales_chart_ai import SalesChartAI


class ChartService:

    def __init__(self, df):

        self.df = df

    def generate(self):

        sales_chart = SalesChartAI(self.df).generate()

        return {
            "salesChart": sales_chart
        }


def generate_charts(df):

    return ChartService(df).generate()