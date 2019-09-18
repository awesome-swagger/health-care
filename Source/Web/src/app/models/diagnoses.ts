import { MomentInput } from 'moment';

import { IDiagnosis } from './diagnosis';
import { IHaveId } from './ihave-id';

export interface IDiagnoses extends IHaveId {
  date_identified?: MomentInput;
  diagnosing_practitioner?: string;
  diagnosis?: string;
  diagnosis_object?: IDiagnosis;
  facility?: string;
  hidden?: boolean;
  is_chronic?: boolean;
  isModified?: boolean;
  original?: boolean;
  patient?: string;
  showTip?: boolean;
  type?: string;
}
