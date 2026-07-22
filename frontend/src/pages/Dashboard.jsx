import { useEffect, useState } from "react";

import KPISection from "../components/KPISection";
import SalesChart from "../components/SalesChart";

import AISummary from "../components/AISummary";
import ReportButton from "../components/ReportButton";

import XAIInsights from "../components/XAIInsights";

export default function Dashboard() {

    const [data, setData] =
        useState(null);
    console.log("Sales Chart:", data?.recommended_charts);
    console.log("Forecast Chart:", data?.forecast_chart);
    console.log(
        "Feature Importance:",
        data?.feature_importance
    );

    console.log(
        "SHAP Data:",
        data?.shap_data
    );

    console.log(
        "XAI Explanation:",
        data?.xai_explanation
    );

    console.log(
        "Insights:",
        data?.insights
    );


    // LOAD DATA


    useEffect(() => {

        const uploaded =
            localStorage.getItem(
                "datasetUploaded"
            );

        const storedData =
            localStorage.getItem(
                "dashboardData"
            );

        if (
            uploaded === "true" &&
            storedData
        ) {

            setData(
                JSON.parse(
                    storedData
                )
            );

        } else {

            setData(null);
        }

    }, []);


    // CLEAR DATA FUNCTION


    const clearDataset = () => {

        localStorage.removeItem(
            "dashboardData"
        );

        localStorage.removeItem(
            "datasetUploaded"
        );

        setData(null);
    };


    // NO DATA SCREEN


    if (!data) {

        return (

            <div
                className="
                    min-h-screen
                    flex
                    items-center
                    justify-center
                    bg-cover
                    bg-center
                    p-8
                "

                style={{
                    backgroundImage:
                        "url('https://www.bitrix24.com/upload/iblock/e3a/mz8n7op1vwwqob6g8ycs5albkzh4i721.jpg')"
                }}
            >

                <div className="
                    bg-white/90
                    backdrop-blur-lg
                    p-12
                    rounded-3xl
                    shadow-2xl
                    text-center
                    max-w-xl
                ">

                    <div className="
                        text-7xl
                        mb-6
                    ">

                        📊

                    </div>

                    <h1 className="
                        text-5xl
                        font-extrabold
                        text-slate-800
                    ">

                        No Dataset Uploaded

                    </h1>

                    <p className="
                        mt-5
                        text-slate-600
                        text-xl
                    ">

                        Upload a dataset
                        to generate AI-powered
                        insights and analytics

                    </p>

                </div>

            </div>
        );
    }

    return (

        <div
            id="dashboard"

            className="
                min-h-screen
                
               bg-gradient-to-br from-gray-700 to-yellow-600
                p-8
            "

        >


            {/* HEADER */}


            <div className="
                bg-white/90
                backdrop-blur-lg
                rounded-3xl
                shadow-2xl
                p-8
                flex
                justify-between
                items-center
                mb-10
                border
                border-white/30
            ">

                <div>

                    <h1 className="
                        text-5xl
                        font-extrabold
                        bg-gradient-to-r
                        from-yellow-900
                        to-gray-900
                        bg-clip-text
                        text-transparent
                    ">

                        OptiWise Dashboard

                    </h1>

                    <p className="
                        text-slate-600
                        mt-3
                        text-lg
                        font-medium
                    ">

                        AI-Powered Decision Intelligence System

                    </p>

                </div>

                {/* BUTTONS */}

                <div className="
                    flex
                    gap-4
                ">

                    <ReportButton />

                    <button
                        onClick={
                            clearDataset
                        }

                        className="
                            bg-gradient-to-r
                            from-gray-500
                            to-red-800

                            text-white
                            px-6
                            py-4

                            rounded-2xl
                            font-semibold

                            shadow-xl

                            hover:scale-105
                            hover:shadow-2xl

                            transition-all
                            duration-300

                            cursor-pointer
                        "
                    >

                        🗑 Clear Dataset

                    </button>

                </div>

            </div>


            {/* KPI SECTION */}


            <div className="mb-10">

                <KPISection data={data} />

            </div>


            {/* SALES CHART */}


            <div className="
                bg-white/90
                backdrop-blur-lg
                p-8
                rounded-3xl
                shadow-2xl
                mb-10
                border
                border-white/30

                hover:shadow-yellow-200

                transition-all
                duration-300
            ">

                <h2 className="
                    text-3xl
                    font-bold
                    text-slate-800
                    mb-6
                ">

                    Sales Analytics

                </h2>

                <SalesChart
                    data={data}
                />

            </div>



            {/* XAI INSIGHTS */}


            {
                (
                    data.feature_importance?.length > 0 ||

                    data.shap_data?.length > 0 ||

                    data.xai_explanation
                ) && (

                    <XAIInsights

                        featureImportance={
                            data.feature_importance
                        }

                        shapData={
                            data.shap_data
                        }

                        explanation={
                            data.xai_explanation
                        }

                    />

                )
            }







            {/* AI SUMMARY */}


            <div className="
                bg-white/90
                backdrop-blur-lg
                rounded-3xl
                shadow-2xl
                overflow-hidden
                border
                border-white/30
                mb-10
            ">

                <AISummary
                    summary={data.summary}
                />

            </div>

        </div>
    );
}