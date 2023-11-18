export type BRAND = {
  BagId: string;
  dimension: {
    len: number;
    bread: number;
    heigth: number;
  };
  weight: number;
  anomalyType: string;
  anomalyDescription: string;
  alert: number;
};