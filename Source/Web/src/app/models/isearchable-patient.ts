import { IHaveId } from "./ihaveid";
import { IPatient } from "./patient";
import { IPotentialPatient } from "./potential-patient";

export interface ISearchablePatient extends IHaveId {
  image: string;
  isPotentialPatient: boolean;
  name: string;
  nameLower: string;
  patient: IPatient | IPotentialPatient;
}
