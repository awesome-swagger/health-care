import { ICarePlan } from "./care-plan";
import { INewPatientDetails } from "../components/modals/../../models/inew-patient-details";
import { IPatient } from "./patient";
import { IPotentialPatient } from "./potential-patient";

export interface IPatientEnrollmentResponse {
  carePlan?: ICarePlan;
  patient?: IPatient;
  potentialPatient?: IPotentialPatient;
  potentialPatientId?: string;
}

export interface IPatientEnrollmentModalResponse extends IPatientEnrollmentResponse {
  /** Action taken on current step */
  action: PatientCreationAction;
  /** Last Completed Step */
  step: PatientCreationStep;
  /** New Patient details collected during the enrollment process */
  newPatientDetails?: INewPatientDetails;
}

export enum PatientCreationAction {
  /** Action was canceled for current step - This should check the step and return data */
  Cancel = 0,
  /** User has indicated that they wish to return to the previous step */
  Back = 1,
  /** User wants to proceed to the next step */
  Next = 2,
  /** User has indicated that they wish to proceed with the enrollment process at a later time */
  Later = 3,
  /**  Save potential patient OR Complete enrollment */
  Complete,
}

export enum PatientCreationStep {
  /** Step 1 - Create/Edit basic patient details - should contain a Potential Patient */
  PotentialPatientDetails = 1,
  /** Step 2b - Care and Billing managers assigned, insurance selected, diagnoses added - NewPatientDetails should be present */
  EnrollementDetails = 2,
  /** Step 3 - Prompt to continue with patient enrollment */
  EnrollmentRequired = 3,
  /** Step 4 - Enrollment patient consent and commitment - NewPatientDetails should be present */
  PatientConsent = 4,
  /** Step 2a - Potential patient was created (not added) and now found on potential patients screen - Potential Patient should be present */
  PotentialPatientAdded = 5,
  /** Step 5 - Enrollment has completed and patient is now found on active patients screen - Patient should be present */
  EnrollmentComplete = 6,
}
