import React, {useEffect, useState} from "react";
import {VectorMap} from "@react-jvectormap/core";
import {usAea} from "@react-jvectormap/unitedstates";
import Link from "next/link";
// import {call} from "apexcharts";

const MapOne = () => {
    const [inputValue, setInputValue] = useState('');

    const handleInputChange = (event: { target: { value: React.SetStateAction<string>; }; }) => {
        setInputValue(event.target.value);
    };
    let content = <div id={
        "mydiv"
    }>

    </div>;

    const callIt = async () => {
        try {
            const response = await fetch(`http://localhost:3000/predict?param=${encodeURIComponent(inputValue)}`);
            const data = await response.json();
            console.log(data);
            // content = (<div>
            //     <p>{data}</p>
            // </div>);
            const div = document.getElementById("mydiv");
            if (div) {
                // append to existing div content
                div.innerHTML += (
                    `<p><b>AeroBot</b>: ${data}</p>`
                );

            }
        } catch (error) {
            console.error('Error:', error);
        }
    };


    return (
        <div
            // auto width
            style={{width: "100%"}}
            className="col-span-12 rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark xl:col-span-7">

            <h4 className="mb-2 text-xl font-semibold text-black dark:text-white">
                AI chatbot
            </h4>
            <div id="mapOne" className="mapOne map-btn">

                <div className="relative">
                    <input
                        type="text"
                        value={inputValue}
                        onChange={handleInputChange}
                        placeholder="Ask llama (about GMM we use)..."
                        className="w-full bg-transparent pl-9 pr-4 font-medium focus:outline-none xl:w-125"
                    />
                    <button className="absolute  top-1/2 -translate-y-1/2" onClick={callIt}>
                        <svg
                            className="fill-body hover:fill-primary dark:fill-bodydark dark:hover:fill-primary"
                            width="20"
                            height="20"
                            viewBox="0 0 20 20"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                fillRule="evenodd"
                                clipRule="evenodd"
                                d="M9.16666 3.33332C5.945 3.33332 3.33332 5.945 3.33332 9.16666C3.33332 12.3883 5.945 15 9.16666 15C12.3883 15 15 12.3883 15 9.16666C15 5.945 12.3883 3.33332 9.16666 3.33332ZM1.66666 9.16666C1.66666 5.02452 5.02452 1.66666 9.16666 1.66666C13.3088 1.66666 16.6667 5.02452 16.6667 9.16666C16.6667 13.3088 13.3088 16.6667 9.16666 16.6667C5.02452 16.6667 1.66666 13.3088 1.66666 9.16666Z"
                                fill=""
                            />
                            <path
                                fillRule="evenodd"
                                clipRule="evenodd"
                                d="M13.2857 13.2857C13.6112 12.9603 14.1388 12.9603 14.4642 13.2857L18.0892 16.9107C18.4147 17.2362 18.4147 17.7638 18.0892 18.0892C17.7638 18.4147 17.2362 18.4147 16.9107 18.0892L13.2857 14.4642C12.9603 14.1388 12.9603 13.6112 13.2857 13.2857Z"
                                fill=""
                            />
                        </svg>
                    </button>


                </div>

                {content}
            </div>
        </div>
    );
};

export default MapOne;