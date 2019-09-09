import { MomentInput } from "moment";

import { IBasicUser } from "./basic-user";
import { ICarePlan } from "./care-plan";

export interface IPotentialPatient extends IBasicUser {
  care_plan?: ICarePlan
  created?: MomentInput;
  facility?: Array<string>;
  modified?: MomentInput;
  patient_profile?: any; // TODO: determine what type of object is returned
  source?: string;
}
