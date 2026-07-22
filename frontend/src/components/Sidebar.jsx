import { NavLink } from "react-router-dom";


export default function Sidebar() {

    const navStyle = ({ isActive }) =>

        `
        block
        px-5
        py-4
        rounded-2xl
        font-medium
        text-lg
        font-bold
        transition-all
        duration-300
        cursor-pointer

        ${isActive
            ? `
                bg-gradient-to-r
                from-yellow-800
                to-gray-500
                text-white
                font-bold
                shadow-xl
                scale-105
              `
            : `
                text-slate-700
                hover:bg-white
                hover:shadow-lg
                hover:text-yellow-600
                hover:scale-105
              `
        }
    `;

    return (

        <div className="
            w-64
            min-h-screen
            bg-gradient-to-b
            from-slate-50
            to-slate-100
            p-6
            shadow-2xl
            border-r
            border-slate-200
        ">

            {/* LOGO */}

            <div className="
                mb-10
                p-5
                rounded-full
                bg-gradient-to-r
                from-gray-600
                to-yellow-800
                shadow-lg
                text-center
            ">

                <h1 className="
                    text-white
                    font-extrabold
                    text-3xl
                    tracking-wide
                ">
                    OptiWise
                </h1>

                <p className="
                    text-yellow-100
                    text-sm
                    
                    mt-1
                ">
                    AI Analytics Platform
                </p>

            </div>

            {/* MENU */}

            <div className="
                flex
                flex-col
                gap-4
            ">

                <NavLink
                    to="/"
                    className={navStyle}
                >
                    Upload
                </NavLink>

                <NavLink
                    to="/dashboard"
                    className={navStyle}
                >
                    Dashboard
                </NavLink>

                <NavLink
                    to="/ask"
                    className={navStyle}
                >
                    Ask Data
                </NavLink>
                <NavLink
                    to="/explorer"
                    className={navStyle}
                >
                    Dataset Explorer
                </NavLink>

            </div>

        </div>
    );
}