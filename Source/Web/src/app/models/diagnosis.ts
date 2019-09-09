import { IHaveId } from "./ihaveid";

export interface IDiagnosis extends IHaveId {
  dx_code?: string;
  name?: string;
}
