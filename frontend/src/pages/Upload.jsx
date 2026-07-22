import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function Upload() {

    const navigate = useNavigate();

    const [loading, setLoading] =
        useState(false);

    const [selectedFile, setSelectedFile] =
        useState(null);

    const [message, setMessage] =
        useState("");

    const upload = async () => {

        if (!selectedFile) {

            setMessage(
                "Please select a file"
            );

            return;
        }


        try {

            setLoading(true);


            const formData = new FormData();


            formData.append(
                "file",
                selectedFile
            );


            const API = import.meta.env.VITE_API_URL;


            const res = await axios.post(
                `${API}/upload`,
                formData,
                {
                    headers: {
                        "Content-Type":
                            "multipart/form-data"
                    }
                }
            );


            console.log(
                "UPLOAD RESPONSE:",
                res.data
            );


            localStorage.setItem(

                "dashboardData",

                JSON.stringify(
                    res.data
                )

            );


            localStorage.setItem(

                "datasetUploaded",

                "true"

            );


            setMessage(
                "Dataset uploaded successfully"
            );


            setTimeout(() => {

                navigate(
                    "/dashboard"
                );

            }, 1200);



        } catch (err) {


            console.log(
                "UPLOAD ERROR:",
                err.response?.data || err.message
            );


            setMessage(
                "Upload failed"
            );


        } finally {


            setLoading(false);

        }

    };

    return (

        <div
            className="
                min-h-screen
                flex
                items-center
                justify-center
                bg-gradient-to-br from-yellow-900 to-gray-600
                p-8
            "


        >

            {/* MAIN CONTENT */}

            <div className="
                w-full
                max-w-2xl
            ">

                {/* HEADER */}

                <div className="
                    text-center
                    mb-10
                ">

                    <h1 className="
                        text-6xl
                        font-extrabold
                        text-white
                        drop-shadow-2xl
                    ">

                        Upload Dataset

                    </h1>

                    <p className="
                        text-white
                        mt-4
                        text-xl
                        font-medium
                    ">

                        Import your business data
                        and generate AI insights

                    </p>

                </div>

                {/* UPLOAD CARD */}

                <div className="
                    bg-white/90
                    backdrop-blur-lg
                    border-2
                border-yellow-500
                    rounded-3xl
                    shadow-2xl
                    p-10
                ">

                    {/* ICON */}

                    <div className="
                        flex
                        justify-center
                        mb-8
                    ">

                        <div className="
                            w-24
                            h-24
                            rounded-full
                            bg-gradient-to-r
                            from-gray-500
                            to-yellow-800
                            flex
                            items-center
                            justify-center
                            text-5xl
                            shadow-2xl
                        ">

                            📂

                        </div>

                    </div>

                    {/* FILE INPUT */}

                    <div className="mb-6">

                        <label className="
                            text-slate-800
                            font-semibold
                            text-lg
                            block
                            mb-3
                        ">

                            Choose Dataset File

                        </label>

                        <input
                            type="file"

                            onChange={(e) =>
                                setSelectedFile(
                                    e.target.files[0]
                                )
                            }

                            className="
                                w-full
                                bg-slate-100
                                border
                                border-slate-300
                                text-slate-700
                                p-4
                                rounded-2xl
                                shadow-lg
                                cursor-pointer

                                file:bg-yellow-900
                                file:text-white
                                file:border-0
                                file:px-4
                                file:py-2
                                file:rounded-xl
                                file:mr-4
                                file:cursor-pointer

                                hover:file:bg-gray-600
                            "
                        />

                    </div>

                    {/* FILE NAME */}

                    {
                        selectedFile && (

                            <div className="
                                bg-slate-100
                                border
                                border-slate-300
                                rounded-2xl
                                p-4
                                text-slate-700
                                mb-6
                                shadow-lg
                            ">

                                📄 {selectedFile.name}

                            </div>
                        )
                    }

                    {/* BUTTON */}

                    <button

                        onClick={upload}

                        disabled={loading}

                        className="
                            w-full
                            bg-gradient-to-r
                            from-gray-500
                            to-yellow-800
                            text-white
                            py-4
                            rounded-2xl
                            text-xl
                            font-bold
                            shadow-2xl

                            hover:scale-105
                            hover:shadow-gray-500/40

                            transition-all
                            duration-300
                            cursor-pointer

                            disabled:opacity-50
                        "
                    >

                        {
                            loading

                                ? "Uploading..."

                                : "Upload Dataset"
                        }

                    </button>

                    {/* MESSAGE */}

                    {
                        message && (

                            <div className="
                                mt-6
                                text-center
                                text-lg
                                font-medium
                                text-slate-800
                            ">

                                {message}

                            </div>
                        )
                    }

                </div>

            </div>

        </div>
    );
}