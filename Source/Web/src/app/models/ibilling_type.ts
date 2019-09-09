import { MomentInput } from "moment";

export interface IBillingType {
  acronym?: string;
  billable_minutes?: number;
  created?: MomentInput;
  id?: string;
  isChronic?: boolean;
  modified?: MomentInput;
  name?: string;
}
