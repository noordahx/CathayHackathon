import { BRAND } from "@/types/brand";
import Image from "next/image";

const brandData: BRAND[] =  [
  {
    BagId: "BAG001",
    dimension: {
      len: 50,
      bread: 30,
      heigth: 25,
    },
    weight: 20,
    anomalyType: "No Anomaly",
    anomalyDescription: "No irregularities detected in the bag.",
  },
  {
    BagId: "BAG002",
    dimension: {
      len: 60,
      bread: 40,
      heigth: 35,
    },
    weight: 18,
    anomalyType: "Low Alert",
    anomalyDescription: "Minor irregularity detected in the bag.",
  },
  {
    BagId: "BAG003",
    dimension: {
      len: 55,
      bread: 32,
      heigth: 28,
    },
    weight: 22,
    anomalyType: "High Alert",
    anomalyDescription: "Significant irregularity detected in the bag. Requires further inspection.",
  },
  {
    BagId: "BAG004",
    dimension: {
      len: 48,
      bread: 28,
      heigth: 24,
    },
    weight: 19,
    anomalyType: "No Anomaly",
    anomalyDescription: "No irregularities detected in the bag.",
  },
  {
    BagId: "BAG005",
    dimension: {
      len: 65,
      bread: 42,
      heigth: 38,
    },
    weight: 17,
    anomalyType: "No Anomaly",
    anomalyDescription: "No irregularities detected in the bag.",
  },
  
];

const TableOne = () => {
  return (
    <div className="rounded-sm border border-stroke bg-white px-5 pt-6 pb-2.5 shadow-default dark:border-strokedark dark:bg-boxdark sm:px-7.5 xl:pb-1">
      <h4 className="mb-6 text-xl font-semibold text-black dark:text-white">
        List of Bags
      </h4>

      <div className="flex flex-col">
  <div className="grid grid-cols-3 rounded-sm bg-gray-2 dark:bg-meta-4 sm:grid-cols-5">
    <div className="p-2.5 xl:p-5">
      <h5 className="text-sm font-medium uppercase xsm:text-base">
        Bag Id
      </h5>
    </div>
    <div className="p-2.5 text-center sm:block xl:p-5">
      <h5 className="text-sm font-medium uppercase xsm:text-base">
        Dimension
      </h5>
    </div>
    <div className="p-2.5 text-center sm:block xl:p-5">
      <h5 className="text-sm font-medium uppercase xsm:text-base">
        Weight
      </h5>
    </div>
    <div className="p-2.5 text-center sm:block xl:p-5">
      <h5 className="text-sm font-medium uppercase xsm:text-base">
        Anomaly Type
      </h5>
    </div>
    <div className="p-2.5 text-center sm:block xl:p-5">
      <h5 className="text-sm font-medium uppercase xsm:text-base">
        Anomaly Description
      </h5>
    </div>
  </div>
</div>

        {brandData.map((brand, key) => (
          <div
            className={`grid grid-cols-3 sm:grid-cols-5 ${
              key === brandData.length - 1
                ? ""
                : "border-b border-stroke dark:border-strokedark"
            }`}
            key={key}
          >
            <div className="flex items-center gap-3 p-2.5 xl:p-5">
              
              <p className="hidden text-black dark:text-white sm:block">
                {brand.BagId}
              </p>
            </div>
            
            <div className="hidden items-center justify-center p-2.5 sm:flex xl:p-5">
              <p className="text-meta-5">{brand.dimension.len},{brand.dimension.bread},{brand.dimension.heigth}</p>
            </div>

            <div className="flex items-center justify-center p-2.5 xl:p-5">
              <p className="text-black dark:text-white">{brand.weight}</p>
            </div>

            <div className="flex items-center justify-center p-2.5 xl:p-5">
              <p className="text-meta-3">{brand.anomalyType}</p>
            </div>

            <div className="hidden items-center justify-center p-2.5 sm:flex xl:p-5">
              <p className="text-black dark:text-white">{brand.anomalyDescription}</p>
            </div>

            
          </div>
        ))}
      </div>
    
  );
};

export default TableOne;
