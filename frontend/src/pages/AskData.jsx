import { useState } from "react";
import axios from "axios";

export default function AskData() {

    const [q, setQ] = useState("");
    const [messages, setMessages] = useState([]);
    const [loading, setLoading] = useState(false);

    const ask = async () => {

        if (!q.trim()) return;

        // USER MESSAGE

        const userMessage = {
            role: "user",
            text: q
        };

        setMessages((prev) => [
            ...prev,
            userMessage
        ]);

        const currentQuestion = q;

        setQ("");

        setLoading(true);

        try {

            const API = import.meta.env.VITE_API_URL;

            const response = await axios.post(
                `${API}/ask`,
                {
                    question: currentQuestion
                }
            );

            // AI MESSAGE

            const aiMessage = {
                role: "ai",
                text:
                    response.data.answer
            };

            setMessages((prev) => [
                ...prev,
                aiMessage
            ]);

        } catch (error) {

            console.log(error);

            const errorMessage = {
                role: "ai",
                text:
                    "AI server error. Please check backend."
            };

            setMessages((prev) => [
                ...prev,
                errorMessage
            ]);

        } finally {

            setLoading(false);
        }
    };

    // ENTER KEY SUPPORT

    const handleKeyDown = (e) => {

        if (e.key === "Enter") {

            ask();
        }
    };
    const handleSuggestion = (question) => {
        setQ(question);

        setTimeout(() => {
            const input = document.querySelector("input");
            if (input) input.focus();
        }, 100);
    };

    return (

        <div
            className="
                min-h-screen
                p-8
                bg-cover
                bg-fixed
                 bg-gradient-to-r from-yellow-950 to-gray-700
            "

            style={{
                backgroundImage:
                    "url('https://www.cumanagement.com/sites/default/files/2021-08/hand-chatbot-technology-background.jpg')"
            }}
        >

            {/* MAIN CONTENT */}

            <div className="
                h-[95vh]
                flex
                flex-col
            ">

                {/* HEADER */}

                <div className="
                    mb-6
                ">

                    <h1 className="
                        text-5xl
                        font-extrabold
                        text-white/90
                        drop-shadow-lg
                    ">

                        AI Data Assistant

                    </h1>

                    <p className="
                        text-white/50
                        mt-3
                        text-lg
                        font-medium
                    ">

                        Ask intelligent questions
                        about your dataset

                    </p>

                </div>

                {/* CHAT CONTAINER */}

                <div className="
                    flex-1
                    bg-white/10
                    backdrop-blur-lg
                    border
                    border-white/30
                    rounded-3xl
                    shadow-2xl
                    p-6
                    overflow-y-auto
                ">

                    {
                        messages.length === 0 && (

                            <div className="
                                text-center
                                mt-16
                            ">

                                <h2 className="
                                    text-4xl
                                    font-extrabold
                                    text-yellow-50
                                ">

                                    Welcome to OptiWise AI


                                </h2>

                                <p className="
                                    text-slate-950
                                    font-extrabold
                                    mt-4
                                    text-lg
                                ">

                                    Ask questions about your dataset

                                </p>

                                {/* EXAMPLE CARDS */}

                                {/* SUGGESTION SECTION */}

                                <div
                                    className="
        mt-10
        max-w-4xl
        mx-auto
        bg-white/10
        backdrop-blur-md
        border
        border-white/20
        rounded-3xl
        p-8
        shadow-2xl
    "
                                >

                                    <h3
                                        className="
            text-3xl
            font-bold
            text-slate-950
            mb-6
        "
                                    >
                                        Questions
                                    </h3>

                                    <div
                                        className="
            flex
            flex-wrap
            gap-4
            justify-center
        "
                                    >

                                        <button
                                            onClick={() =>
                                                handleSuggestion(
                                                    "What is the total sales?"
                                                )
                                            }
                                            className="
                bg-gray-50
                border
                border-yellow-50
                px-6
                py-3
                rounded-full
                text-slate-700
                font-medium
                shadow-lg
                hover:scale-105
                transition-all
                duration-300
            "
                                        >
                                            Total Sales
                                        </button>

                                        <button
                                            onClick={() =>
                                                handleSuggestion(
                                                    "Show profit analysis"
                                                )
                                            }
                                            className="
                bg-gray-50
                border
                border-yellow-100
                px-6
                py-3
                rounded-full
                text-slate-700
                font-medium
                shadow-lg
                hover:scale-105
                transition-all
                duration-300
            "
                                        >
                                            Profit Analysis
                                        </button>

                                        <button
                                            onClick={() =>
                                                handleSuggestion(
                                                    "Give dataset summary"
                                                )
                                            }
                                            className="
                bg-gray-50
                border
                border-yellow-100
                px-6
                py-3
                rounded-full
                text-slate-700
                font-medium
                shadow-lg
                hover:scale-105
                transition-all
                duration-300
            "
                                        >
                                            Dataset Summary
                                        </button>

                                        <button
                                            onClick={() =>
                                                handleSuggestion(
                                                    "Provide business insights"
                                                )
                                            }
                                            className="
                bg-gray-50
                border
                border-yellow-100
                px-6
                py-3
                rounded-full
                text-slate-700
                font-medium
                shadow-lg
                hover:scale-105
                transition-all
                duration-300
            "
                                        >
                                            Business Insights
                                        </button>

                                        <button
                                            onClick={() =>
                                                handleSuggestion(
                                                    "Show top performing categories"
                                                )
                                            }
                                            className="
                bg-gray-50
                border
                border-yellow-100
                px-6
                py-3
                rounded-full
                text-slate-700
                font-medium
                shadow-lg
                hover:scale-105
                transition-all
                duration-300
            "
                                        >
                                            Top Categories
                                        </button>

                                        <button
                                            onClick={() =>
                                                handleSuggestion(
                                                    "What are the key recommendations?"
                                                )
                                            }
                                            className="
                bg-gray-50
                border
                border-yellow-100
                px-6
                py-3
                rounded-full
                text-slate-700
                font-medium
                shadow-lg
                hover:scale-105
                transition-all
                duration-300
            "
                                        >
                                            Recommendations
                                        </button>

                                    </div>

                                </div>
                            </div>
                        )
                    }

                    {/* CHAT MESSAGES */}

                    <div className="space-y-5">

                        {
                            messages.map(
                                (
                                    msg,
                                    index
                                ) => (

                                    <div
                                        key={index}
                                        className={`
                                            flex
                                            ${msg.role ===
                                                "user"

                                                ? "justify-end"

                                                : "justify-start"
                                            }
                                        `}
                                    >

                                        <div
                                            className={`
                                                px-6
                                                py-4
                                                rounded-3xl
                                                max-w-[75%]
                                                whitespace-pre-wrap
                                                shadow-xl
                                                text-lg

                                                ${msg.role ===
                                                    "user"

                                                    ? `
                                                            bg-gradient-to-r
                                                            from-yellow-800
                                                            to-gray-500
                                                            text-white
                                                          `

                                                    : `
                                                            bg-slate-100
                                                            border
                                                            border-slate-200
                                                            text-slate-700
                                                          `
                                                }
                                            `}
                                        >

                                            {msg.text}

                                        </div>

                                    </div>
                                )
                            )
                        }

                        {/* LOADING */}

                        {
                            loading && (

                                <div className="
                                    flex
                                    justify-start
                                ">

                                    <div className="
                                        bg-slate-100
                                        text-slate-700
                                        px-6
                                        py-4
                                        rounded-3xl
                                        shadow-lg
                                        border
                                        border-slate-200
                                    ">

                                        AI Thinking...

                                    </div>

                                </div>
                            )
                        }

                    </div>

                </div>

                {/* INPUT AREA */}

                <div className="
                    flex
                    gap-4
                    mt-6
                ">

                    <input
                        type="text"

                        value={q}

                        onChange={(e) =>
                            setQ(
                                e.target.value
                            )
                        }

                        onKeyDown={
                            handleKeyDown
                        }

                        placeholder="
                            Ask anything about your dataset...
                        "

                        className="
                            flex-1
                            bg-white
                            border
                            border-slate-300
                            text-slate-900
                            placeholder-slate-400
                            p-4
                            rounded-2xl
                            outline-none
                            focus:ring-2
                            focus:ring-yellow-100
                            shadow-lg
                            text-lg
                        "
                    />

                    <button
                        onClick={ask}
                        disabled={loading}
                        className="
                            bg-gradient-to-r
                            from-gray-500
                            to-yellow-700
                            text-white
                            px-10
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

                        Send

                    </button>

                </div>

            </div>

        </div>
    );
}