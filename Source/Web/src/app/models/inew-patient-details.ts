import { IBillingType } from "./ibilling_type";
import { ICarePlan } from "./care-plan";
import { IDiagnoses } from "./diagnoses";
import { IDiagnosis } from "./diagnosis";
import { IEmployee } from "./employee";
import { IEnrollmentConsentDetails } from "./ienrollment-consent-details";
import { IFacility } from "./facility";
import { IInsurance } from './insurance';
import { IPatient } from "./patient";
import { IPotentialPatient } from "./potential-patient";
import { IRole } from "./role";
import { IServiceArea } from "./service-area";

export interface INewPatientDetails {
  billingPractioner?: IEmployee;
  careManager?: IEmployee;
  carePlan?: ICarePlan;
  carePlanRoles: { [id: string]: { role: IRole, selected: boolean; } };
  checked: {
    enroll?: boolean;
    reimburses?: boolean;
  };
  chronic?: boolean;
  /** A collection of currently assigned diagnoses */
  diagnoses: Array<IDiagnoses>;
  /** A single (new) diagnosis being added to the patient */
  diagnosis?: IDiagnosis;
  email?: string;
  /** ONLY present once */
  enrollmentConsentDetails?: IEnrollmentConsentDetails;
  facility?: IFacility;
  firstName?: string;
  insurance?: IInsurance;
  lastName?: string;
  name?: string,
  patient: {
    isPotential: boolean,
    isPreload?: boolean,
    patient?: IPotentialPatient | IPatient
  };
  phoneNumber?: string;
  planType?: IBillingType;
  serviceArea?: IServiceArea;
  source?: string;
}
