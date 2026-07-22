export default function XAIInsights({

    featureImportance = [],

    shapData = [],

    explanation = ""

}) {

    return (

        <div className="
            bg-white/90
            backdrop-blur-lg
            p-8
            rounded-3xl
            shadow-2xl
            mb-10
            border
            border-white/30
        ">

            <h1 className="
                text-4xl
                font-bold
                text-slate-900
                mb-6
            ">

                Explainable AI Insights

            </h1>

            {/* Explanation */}

            <div className="mb-8">

                <h2 className="
                    text-2xl
                    font-semibold
                    mb-3
                ">

                    AI Explanation

                </h2>

                <p className="
                    text-slate-700
                    text-lg
                ">

                    {explanation}

                </p>

            </div>

            {/* Feature Importance */}

            <div className="mb-8">

                <h2 className="
                    text-2xl
                    font-semibold
                    mb-4
                ">

                    Feature Importance

                </h2>

                {
                    featureImportance.map(
                        (item, index) => (

                            <div
                                key={index}
                                className="mb-4"
                            >

                                <div className="
                                    flex
                                    justify-between
                                    mb-1
                                ">

                                    <span>
                                        {item.feature}
                                    </span>

                                    <span>
                                        {item.importance}
                                    </span>

                                </div>

                                <div className="
                                    w-full
                                    bg-gray-200
                                    rounded-full
                                    h-3
                                ">

                                    <div
                                        className="
                                           bg-gradient-to-r
                from-gray-500
                to-yellow-700
                                            h-3
                                            rounded-full
                                        "

                                        style={{
                                            width:
                                                `${item.importance * 100}%`
                                        }}
                                    />

                                </div>

                            </div>
                        )
                    )
                }

            </div>


        </div>
    );
}