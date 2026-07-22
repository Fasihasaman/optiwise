import { useEffect, useMemo, useState } from "react";
import axios from "axios";

export default function DatasetExplorer() {
    const [datasetName, setDatasetName] = useState("");
    const [rows, setRows] = useState([]);
    const [columns, setColumns] = useState([]);
    const [statistics, setStatistics] = useState({});

    const [loading, setLoading] = useState(true);

    // Input values
    const [search, setSearch] = useState("");
    const [filterColumn, setFilterColumn] = useState("");
    const [filterValue, setFilterValue] = useState("");
    const [sortColumn, setSortColumn] = useState("");
    const [sortOrder, setSortOrder] = useState("asc");

    // Applied values
    const [appliedSearch, setAppliedSearch] = useState("");
    const [appliedFilterColumn, setAppliedFilterColumn] = useState("");
    const [appliedFilterValue, setAppliedFilterValue] = useState("");
    const [appliedSortColumn, setAppliedSortColumn] = useState("");
    const [appliedSortOrder, setAppliedSortOrder] = useState("asc");
    const [page, setPage] = useState(1);

    const [selectedRow, setSelectedRow] = useState(null);

    const rowsPerPage = 10;

    useEffect(() => {

        loadDataset();

    }, []);

    const loadDataset = async () => {

        try {

            setLoading(true);

            const API = import.meta.env.VITE_API_URL;

            await axios.get(
                `${API}/dataset-explorer`
            );
            console.log(res.data);
            setRows(res.data.sample || []);

            setColumns(res.data.columns || []);

            setStatistics(res.data.statistics || {});
            setDatasetName(res.data.dataset_name || "Uploaded Dataset");

        } catch (e) {

            console.log(e);

        }

        setLoading(false);

    };

    const uniqueValues = useMemo(() => {

        if (!filterColumn) return [];

        return [...new Set(

            rows.map(r => r[filterColumn])

        )]
            .filter(Boolean)
            .slice(0, 100);

    }, [rows, filterColumn]);

    const filteredRows = useMemo(() => {

        let data = [...rows];

        if (appliedSearch !== "") {

            data = data.filter(row =>

                Object.values(row).some(value =>

                    String(value)
                        .toLowerCase()
                        .includes(appliedSearch.toLowerCase())

                )

            );

        }

        if (appliedFilterColumn && appliedFilterValue) {

            data = data.filter(

                row =>

                    String(row[appliedFilterColumn]) ===

                    String(filterValue)

            );

        }

        if (appliedSortColumn) {

            data.sort((a, b) => {

                let A = a[appliedSortColumn];

                let B = b[appliedSortColumn];

                if (!isNaN(A) && !isNaN(B)) {

                    return appliedSortOrder === "asc"

                        ? Number(A) - Number(B)

                        : Number(B) - Number(A);

                }

                return appliedSortOrder === "asc"

                    ? String(A).localeCompare(String(B))

                    : String(B).localeCompare(String(A));

            });

        }

        return data;

    }, [
        rows,
        appliedSearch,
        appliedFilterColumn,
        appliedFilterValue,
        appliedSortColumn,
        appliedSortOrder
    ]);

    const totalPages = Math.ceil(

        filteredRows.length /

        rowsPerPage

    );

    const currentRows = filteredRows.slice(

        (page - 1) * rowsPerPage,

        page * rowsPerPage

    );

    useEffect(() => {

        setPage(1);

    }, [

        search,

        filterColumn,

        filterValue,

        sortColumn,

        sortOrder

    ]);

    const displayColumns = useMemo(() => {

        if (columns.length <= 8)

            return columns;

        return columns.slice(0, 8);

    }, [columns]);

    if (loading) {

        return (

            <div className="text-center py-16 text-xl">

                Loading Dataset...

            </div>

        );

    }

    return (

        <div className="bg-white rounded-3xl shadow-xl p-8">

            <div className="flex justify-between items-center mb-8">

                <div>

                    <h1 className="text-4xl font-bold text-gray-900">
                        Interactive Dataset Explorer
                    </h1>

                    <p className="mt-2 text-black font-semibold text-lg">
                        Explore, search, filter and analyze your uploaded dataset.
                    </p>

                </div>

                <div
                    className="
            bg-gradient-to-r
            from-yellow-700
            to-yellow-500
            text-white
            px-6
            py-4
            rounded-2xl
            shadow-lg
            min-w-[260px]
        "
                >

                    <p className="text-sm uppercase tracking-wider opacity-90">
                        Dataset
                    </p>

                    <h2
                        className="
                text-xl
                font-bold
                truncate
            "
                        title={datasetName}
                    >
                        {datasetName}
                    </h2>

                </div>

            </div>

            {/* Toolbar */}

            <div className="grid lg:grid-cols-5 gap-4 mb-8">


                <input

                    value={search}

                    onChange={(e) =>

                        setSearch(e.target.value)

                    }

                    placeholder="Search..."

                    className="border-2 border-yellow-800 bg-gray-50 rounded-xl p-3 font-bold text-l cursor-pointer"

                />

                <select

                    value={filterColumn}

                    onChange={(e) => {

                        setFilterColumn(

                            e.target.value

                        );

                        setFilterValue("");

                    }}

                    className="border-2 border-yellow-800 bg-gray-50 rounded-xl p-3 font-bold text-l cursor-pointer"

                >

                    <option value="">

                        Filter Column

                    </option>

                    {

                        columns.map(col => (

                            <option

                                key={col}

                                value={col}

                            >

                                {col}

                            </option>

                        ))

                    }

                </select>

                <select

                    value={filterValue}

                    onChange={(e) =>

                        setFilterValue(

                            e.target.value

                        )

                    }

                    className="border-2 border-yellow-800 bg-gray-50 rounded-xl p-3 font-bold text-l cursor-pointer"

                >

                    <option value="">

                        Filter Value

                    </option>

                    {

                        uniqueValues.map(v => (

                            <option

                                key={v}

                                value={v}

                            >

                                {String(v)}

                            </option>

                        ))

                    }

                </select>

                <select

                    value={sortColumn}

                    onChange={(e) =>

                        setSortColumn(

                            e.target.value

                        )

                    }

                    className="border-2 border-yellow-800 bg-gray-50 rounded-xl p-3 font-bold text-l cursor-pointer"

                >

                    <option value="">

                        Sort By

                    </option>

                    {

                        columns.map(col => (

                            <option

                                key={col}

                                value={col}

                            >

                                {col}

                            </option>

                        ))

                    }

                </select>

                <select

                    value={sortOrder}

                    onChange={(e) =>

                        setSortOrder(

                            e.target.value

                        )

                    }

                    className="border-2 border-yellow-800 bg-gray-50 rounded-xl p-3 font-bold text-l cursor-pointer"

                >

                    <option value="asc">

                        Ascending

                    </option>

                    <option value="desc">

                        Descending

                    </option>

                </select>

            </div>
            <div className="flex gap-4 mb-8">

                <button
                    onClick={() => {

                        setAppliedSearch(search);
                        setAppliedFilterColumn(filterColumn);
                        setAppliedFilterValue(filterValue);
                        setAppliedSortColumn(sortColumn);
                        setAppliedSortOrder(sortOrder);

                        setPage(1);

                    }}
                    className="
            px-6
            py-3
            rounded-xl
            bg-gradient-to-r
            from-yellow-700
            to-yellow-500
            text-white
            font-semibold
            hover:scale-105
            transition
            shadow-lg
            cursor-pointer
            hover:text-black
        "
                >
                    Apply Filters
                </button>

                <button
                    onClick={() => {

                        setSearch("");
                        setFilterColumn("");
                        setFilterValue("");
                        setSortColumn("");
                        setSortOrder("asc");

                        setAppliedSearch("");
                        setAppliedFilterColumn("");
                        setAppliedFilterValue("");
                        setAppliedSortColumn("");
                        setAppliedSortOrder("asc");

                        setPage(1);

                    }}
                    className="
            px-6
            py-3
            rounded-xl
            cursor-pointer
            bg-gray-600
            text-white
            hover:bg-gray-400
            hover:text-black
            font-semibold
        "
                >
                    Reset
                </button>

            </div>
            {/*  TABLE  */}

            <div className="overflow-x-auto rounded-2xl border border-gray-200">

                <table className="min-w-full">

                    <thead className="bg-yellow-600 text-white">

                        <tr>

                            {

                                displayColumns.map(col => (

                                    <th
                                        key={col}
                                        className="
                                            px-5
                                            py-4
                                            text-xl
                                            text-
                                            text-left
                                            font-bold
                                            whitespace-nowrap
                                        "
                                    >

                                        {col}

                                    </th>

                                ))

                            }

                        </tr>

                    </thead>

                    <tbody>

                        {

                            currentRows.length === 0 ?

                                (

                                    <tr>

                                        <td
                                            colSpan={displayColumns.length}
                                            className="
                                                text-center
                                                py-12
                                                font-bold
                                                text-gray-500
                                            "
                                        >

                                            No matching records found.

                                        </td>

                                    </tr>

                                )

                                :

                                currentRows.map((row, index) => (

                                    <tr

                                        key={index}

                                        onClick={() =>
                                            setSelectedRow(row)
                                        }

                                        className="
                                            border-b
                                            hover:bg-yellow-50
                                            cursor-pointer
                                            font-medium
                                            text-xl
                                            transition
                                        "

                                    >

                                        {

                                            displayColumns.map(col => (

                                                <td
                                                    key={col}
                                                    className="
                                                        px-5
                                                        py-4
                                                    "
                                                >

                                                    <div className="
                                                        max-w-[220px]
                                                        truncate
                                                    ">

                                                        {

                                                            String(
                                                                row[col] ?? ""
                                                            )

                                                        }

                                                    </div>

                                                </td>

                                            ))

                                        }

                                    </tr>

                                ))

                        }

                    </tbody>

                </table>

            </div>

            {/*  PAGINATION  */}

            <div className="
                flex
                justify-between
                items-center
                mt-6
            ">

                <button

                    disabled={page === 1}

                    onClick={() =>

                        setPage(page - 1)

                    }

                    className="
                        px-5
                        py-2
                        rounded-lg
                        bg-yellow-600
                        text-white
                        disabled:opacity-40
                        cursor-pointer
                        hover:bg-mauve-500
                        font-bold
                    "

                >

                    Previous

                </button>

                <span className=" text-lg font-semibold">

                    Page {page} of {totalPages || 1}

                </span>

                <button

                    disabled={page === totalPages}

                    onClick={() =>

                        setPage(page + 1)

                    }

                    className="
                        px-5
                        py-2
                        rounded-lg
                        bg-yellow-600
                        text-white
                        disabled:opacity-40
                        cursor-pointer
                        hover:bg-mauve-500
                        font-bold
                        
                    "

                >

                    Next

                </button>

            </div>

            {/*  STATISTICS  */}

            {

                Object.keys(statistics).length > 0 &&

                <>

                    <h2 className="
                        text-3xl
                        font-bold
                        mt-12
                        mb-6
                    ">

                        Numeric Statistics

                    </h2>

                    <div className="
                        grid
                        md:grid-cols-2
                        lg:grid-cols-3
                        gap-6
                    ">

                        {

                            Object.entries(statistics).map(

                                ([column, stat]) => (

                                    <div

                                        key={column}

                                        className="
                                            bg-gray-50
                                            rounded-2xl
                                            p-6
                                            shadow
                                        "

                                    >

                                        <h3 className="
                                            text-xl
                                            font-bold
                                            mb-4
                                        ">

                                            {column}

                                        </h3>

                                        <div className="space-y-2">

                                            <p>Mean : {stat.mean}</p>

                                            <p>Median : {stat.median}</p>

                                            <p>Minimum : {stat.min}</p>

                                            <p>Maximum : {stat.max}</p>

                                            <p>Std Dev : {stat.std}</p>

                                        </div>

                                    </div>

                                )

                            )

                        }

                    </div>

                </>

            }

            {/*  DETAILS MODAL  */}

            {

                selectedRow &&

                <div

                    className="
                        fixed
                        text-lg
                        font-semibold
                        inset-0
                        bg-black/60
                        flex
                        justify-center
                        items-center
                        z-50
                    "

                >

                    <div

                        className="
                            bg-white
                            rounded-3xl
                            w-[90%]
                            max-w-5xl
                            max-h-[85vh]
                            overflow-y-auto
                            p-8
                            relative
                        "

                    >

                        <button

                            onClick={() =>

                                setSelectedRow(null)

                            }

                            className="
                                absolute
                                right-6
                                top-6
                                text-5xl
                              
                                mb-6
                                hover:bg-gray-300
                                cursor-pointer
                                font-bold
                            "

                        >

                            ×

                        </button>

                        <h2 className="
                            text-3xl
                            font-bold
                            mb-8
                        ">

                            Record Details

                        </h2>

                        <div className="
                            grid
                            md:grid-cols-2
                            gap-5
                        ">

                            {

                                Object.entries(selectedRow)

                                    .filter(([key]) =>

                                        ![
                                            "img_link",
                                            "product_link",
                                            "review_content"
                                        ].includes(key)

                                    )

                                    .map(([key, value]) => (

                                        <div

                                            key={key}

                                            className="
                                                bg-gray-50
                                                rounded-xl
                                                p-4
                                            "

                                        >

                                            <p className="
                                                font-bold
                                                text-yellow-700
                                                mb-2
                                            ">

                                                {key}

                                            </p>

                                            <p className="
                                                break-words
                                            ">

                                                {

                                                    String(value)

                                                }

                                            </p>

                                        </div>

                                    ))

                            }

                        </div>

                    </div>

                </div>

            }

        </div>

    );

}