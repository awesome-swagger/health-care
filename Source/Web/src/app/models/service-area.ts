import { MomentInput } from "moment";

import { IHaveId } from "./ihaveid";

export interface IServiceArea extends IHaveId {
  care_plans_count?: number;
  created?: MomentInput;
  modified?: MomentInput;
  name?: string;
  plan_templates_count?: number;
}
