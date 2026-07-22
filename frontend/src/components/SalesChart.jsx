import {
    ResponsiveContainer,
    BarChart,
    Bar,
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    LabelList,
} from "recharts";

export default function SalesChart({ data }) {

    if (!data || !data.data || data.data.length === 0) {
        return (
            <div className="h-[450px] flex items-center justify-center text-gray-500 text-lg">
                No Chart Available
            </div>
        );
    }

    const isLine = data.chartType === "line";

    return (

        <div className="w-full">

            {/* Chart Title */}

            <h2 className="text-2xl font-bold text-center mb-5">
                {data.title}
            </h2>

            <div className="w-full h-[450px]">

                <ResponsiveContainer width="100%" height="100%">

                    {

                        isLine ?

                            (

                                <LineChart
                                    data={data.data}
                                    margin={{
                                        top: 20,
                                        right: 30,
                                        left: 20,
                                        bottom: 80
                                    }}
                                >

                                    <CartesianGrid strokeDasharray="3 3" />

                                    <XAxis
                                        dataKey={data.xAxis}
                                        interval={0}
                                        angle={-30}
                                        textAnchor="end"
                                        height={90}
                                        
                                        tick={{ fontSize: 11 }}

                                        tickFormatter={(value) => {

                                            const text = String(value)
                                                .split("|")
                                                .pop();

                                            return text.length > 18
                                                ? text.substring(0, 18) + "..."
                                                : text;
                                        }}

                                        label={{
                                            value: data.xAxis,
                                            position: "insideBottom",
                                            offset: -5,
                                            style: {
                                                fontSize: 15,
                                                fontWeight: "bold"
                                            }
                                        }}

                                    />

                                    <YAxis

                                        width={90}

                                        tick={{
                                            fontSize: 11
                                        }}

                                        tickFormatter={(value) =>
                                            Number(value).toLocaleString()
                                        }

                                        label={{
                                            value: data.yAxis,
                                            angle: -90,
                                            position: "insideLeft",
                                            style: {
                                                fontSize: 15,
                                                fontWeight: "bold"
                                            }
                                        }}

                                    />

                                    <Tooltip

                                        formatter={(value) => [

                                            Number(value).toLocaleString(),

                                            data.yAxis

                                        ]}

                                        labelFormatter={(label, payload) =>
                                            payload?.[0]?.payload?.[data.xAxis]
                                        }

                                    />

                                    <Line
                                        dataKey={data.yAxis}
                                        stroke="#6e4822"
                                        strokeWidth={3}
                                        dot
                                    />

                                </LineChart>

                            )

                            :

                            (

                                <BarChart

                                    data={data.data}

                                    barCategoryGap="30%"

                                    barGap={4}

                                    margin={{
                                        top: 20,
                                        right: 30,
                                        left: 20,
                                        bottom: 80
                                    }}

                                >

                                    <CartesianGrid strokeDasharray="3 3" />

                                    <XAxis

                                        dataKey={data.xAxis}

                                        interval={0}

                                        angle={-30}

                                        textAnchor="end"

                                        height={90}

                                        tick={{
                                            fontSize: 11
                                        }}

                                        tickFormatter={(value) => {

                                            const text = String(value)
                                                .split("|")
                                                .pop();

                                            return text.length > 18
                                                ? text.substring(0, 18) + "..."
                                                : text;

                                        }}

                                        label={{

                                            value: data.xAxis,

                                            position: "insideBottom",

                                            offset: -5,

                                            style: {

                                                fontSize: 15,

                                                fontWeight: "bold"

                                            }

                                        }}

                                    />

                                    <YAxis

                                        width={90}

                                        tick={{
                                            fontSize: 11
                                        }}

                                        tickFormatter={(value) =>
                                            Number(value).toLocaleString()
                                        }

                                        label={{

                                            value: data.yAxis,

                                            angle: -90,

                                            position: "insideLeft",

                                            style: {

                                                fontSize: 15,

                                                fontWeight: "bold"

                                            }

                                        }}

                                    />

                                    <Tooltip

                                        formatter={(value) => [

                                            Number(value).toLocaleString(),

                                            data.yAxis

                                        ]}

                                        labelFormatter={(label, payload) =>
                                            payload?.[0]?.payload?.[data.xAxis]
                                        }

                                    />

                                    <Bar

                                        dataKey={data.yAxis}

                                        fill="#6e4822"

                                        radius={[8, 8, 0, 0]}

                                    >

                                        <LabelList

                                            dataKey={data.yAxis}

                                            position="top"

                                            formatter={(value) =>
                                                Number(value).toLocaleString()
                                            }

                                            fontSize={10}

                                        />

                                    </Bar>

                                </BarChart>

                            )

                    }

                </ResponsiveContainer>

            </div>

        </div>

    );

}