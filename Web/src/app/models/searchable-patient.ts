import { IHaveId } from './ihave-id';
import { IPatient } from './patient';
import { IPotentialPatient } from './potential-patient';

export interface ISearchablePatient extends IHaveId {
  email: string;
  image: string;
  isPotentialPatient: boolean;
  name: string;
  nameLower: string;
  patient: IPatient | IPotentialPatient;
}
