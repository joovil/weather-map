"use client";

export default function SearchButton() {
    return (
        <button className="px-4 py-2 text-white bg-blue-500 rounded-md" onClick={() => {console.log("Search button clicked")
        }}>
        Search
        </button>
    );
    }
