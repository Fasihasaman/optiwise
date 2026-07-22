export default function AISummary({ summary }) {

    return (

        <div className="bg-gradient-to-r from-yellow-900 to-gray-500 text-white p-8 rounded-2xl shadow mt-10">

            <h2 className="text-3xl font-bold">

                AI Executive Summary

            </h2>

            <p className="mt-5 leading-8 text-lg whitespace-pre-wrap">

                {summary}

            </p>

        </div>
    );
}