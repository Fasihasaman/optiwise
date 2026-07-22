export default function KPISection({ data }) {

    const completeness =
        data?.kpis?.data_completeness || 0;

    const quality =
        data?.kpis?.data_quality || "N/A";

    return (

        <div className="
            grid
            grid-cols-1
            sm:grid-cols-2
            lg:grid-cols-4
            gap-6
        ">

            {/* Total Rows */}

            <div className="
                bg-white
                rounded-3xl
                shadow-lg
                p-6
                border-l-8
                border-yellow-600
                hover:shadow-2xl
                hover:-translate-y-1
                transition-all
            ">

                <p className="
                    text-black
                    text-lg
                    font-semibold
                    mb-2
                
                ">
                    Total Rows
                </p>

                <h2 className="
                    text-4xl
                    font-extrabold
                    text-gray-800
                ">
                    {data?.rows || 0}
                </h2>

            </div>

            {/* Total Columns */}

            <div className="
               bg-white
                rounded-3xl
                shadow-lg
                p-6
                border-l-8
                border-yellow-600
                hover:shadow-2xl
                hover:-translate-y-1
                transition-all
            ">

                <p className="
                    text-black
                    text-lg
                    font-semibold
                    mb-2
                
                ">
                    Total Columns
                </p>

                <h2 className="
                    text-4xl
                    font-extrabold
                    text-gray-800
                ">
                    {data?.columns || 0}
                </h2>

            </div>

            {/* Missing Values */}

            <div className="
 bg-white
                rounded-3xl
                shadow-lg
                p-6
                border-l-8
                border-yellow-600
                hover:shadow-2xl
                hover:-translate-y-1
                transition-all
">

                <p className="text-lg font-semibold mb-2">
                    Missing Values
                </p>

                <h2 className="text-4xl font-extrabold text-red-600">
                    {data?.kpis?.missing_values ?? 0}
                </h2>

            </div>

            {/* Memory Usage */}

            <div className="
 bg-white
                rounded-3xl
                shadow-lg
                p-6
                border-l-8
                border-yellow-600
                hover:shadow-2xl
                hover:-translate-y-1
                transition-all
">

                <p className="text-lg font-semibold mb-2">
                    Memory Usage
                </p>

                <h2 className="text-4xl font-extrabold text-black">
                    {data?.kpis?.memory_usage ?? 0} MB
                </h2>

            </div>

        </div>

    );

}