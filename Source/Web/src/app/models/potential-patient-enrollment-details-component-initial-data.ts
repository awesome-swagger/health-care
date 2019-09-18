import { INewPatientDetails } from './new-patient-details';
import { IPotentialPatient } from './potential-patient';

export interface IPotentialPatientEnrollmentDetailsComponentInitialData {
  /** Passed from the 'Potential Patient Details Component' */
  newPatientDetails?: INewPatientDetails;
  /** Passed from other forms where a Care Manager would not be present */
  potentialPatient?: IPotentialPatient;
}
