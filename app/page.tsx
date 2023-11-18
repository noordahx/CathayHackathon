import ECommerce from "@/components/Dashboard/E-commerce";
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "AERO Geniuses",
};

export default function Home() {
  return (
    <>
      <ECommerce />
    </>
  );
}
