import { IHaveId } from './ihave-id';

export interface IDiagnosis extends IHaveId {
  dx_code?: string;
  name?: string;
}
