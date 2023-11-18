import React, { useState } from "react";
import { VectorMap } from "@react-jvectormap/core";
import { usAea } from "@react-jvectormap/unitedstates";

const MapOne = () => {
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (event: { target: { value: React.SetStateAction<string>; }; }) => {
    setInputValue(event.target.value);
  };

  const callIt = async () => {
    try {
      const response = await fetch(`http://localhost:3000/predict?param=${encodeURIComponent(inputValue)}`);
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="col-span-12 rounded-sm border border-stroke bg-white py-6 px-7.5 shadow-default dark:border-strokedark dark:bg-boxdark xl:col-span-7">
      <h4 className="mb-2 text-xl font-semibold text-black dark:text-white">
        AI chatbot
      </h4>
      <div id="mapOne" className="mapOne map-btn h-90">
        {/* <VectorMap map={usAea} backgroundColor="#F5F5F5" /> */}
        <input type="text" value={inputValue} onChange={handleInputChange} />
        <button onClick={callIt}>Call it</button>
      </div>
    </div>
  );
};

export default MapOne;