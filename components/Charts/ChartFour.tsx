"use client";
import {ApexOptions} from "apexcharts";
import React, {useState} from "react";
import dynamic from "next/dynamic";

const ApexCharts = dynamic(() => import("react-apexcharts"), {ssr: false});

interface ChartFourState {
    series: { data: number[] }[];
}

const ChartFour: React.FC = () => {
    const [state, setState] = useState<ChartFourState>({
        series: [
            {
                data: [
                    10, 13, 12, 11, 0, 12, 6, 10, 8, 13, 6, 2, 16, 5, 0, 12, 14, 13, 19, 11, 6, 5, 6, 19, 6, 19, 11, 0, 19, 18
                ],
            },
        ],
    });

    // Update the state
    const updateState = () => {
        setState((prevState) => ({
            ...prevState,
            // Update the desired properties
        }));
    };
    updateState;

    const options: ApexOptions = {
        colors: ["#3C50E0"],
        chart: {
            fontFamily: "Satoshi, sans-serif",
            type: "bar",
            height: 350,
            toolbar: {
                show: false,
            },
        },
        plotOptions: {
            bar: {
                horizontal: false,
                columnWidth: "55%",
                // endingShape: "rounded",
                borderRadius: 2,
            },
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            show: true,
            width: 4,
            colors: ["transparent"],
        },
        xaxis: {
            categories: [
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "11",
                "12",
                "13",
                "14",
                "15",
                "16",
                "17",
                "18",
                "19",
                "20",
                "21",
                "22",
                "23",
                "24",
                "25",
                "26",
                "27",
                "28",
                "29",
                "30",
            ],
            axisBorder: {
                show: false,
            },
            axisTicks: {
                show: false,
            },
        },
        legend: {
            show: true,
            position: "top",
            horizontalAlign: "left",
            fontFamily: "inter",

            markers: {
                radius: 99,
            },
        },
        // yaxis: {
        //   title: false,
        // },
        grid: {
            yaxis: {
                lines: {
                    show: false,
                },
            },
        },
        fill: {
            opacity: 1,
        },

        tooltip: {
            x: {
                show: false,
            },
            // y: {
            //   formatter: function (val) {
            //     return val;
            //   },
            // },
        },
    };

    return (
        <div
            className="col-span-12 rounded-sm border border-stroke bg-white px-5 pt-7.5 pb-5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5">
            <div>
                <h3 className="text-xl font-semibold text-black dark:text-white">
                    Monthly alerts
                </h3>
            </div>

            <div className="mb-2">
                <div id="chartFour" className="-ml-5">
                    <ApexCharts
                        options={options}
                        series={state.series}
                        type="bar"
                        height={350}
                    />
                </div>
            </div>
        </div>
    );
};

export default ChartFour;
