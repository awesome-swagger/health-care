import { ICarePlan } from "./care-plan";
import { IFacility } from "./facility";
import { INewPatientDetails } from "./inew-patient-details";
import { IPatient } from "./patient";
import { IPotentialPatient } from "./potential-patient";

export interface IAddPatientToPlanComponentData {
  action?: ('add' | 'edit');
  carePlan?: ICarePlan;
  disableRemovePatient?: boolean;
  enrollPatientChecked?: boolean;
  facility?: IFacility;
  facilityId?: string;
  newPatientDetails?: INewPatientDetails;
  patient?: IPatient;
  potentialPatient?: IPotentialPatient;
}
