import { MomentInput } from 'moment';

import { IHaveId } from './ihave-id';
import { IOrganization } from './organization';

export interface IInsurance extends IHaveId {
  created?: MomentInput;
  modified?: MomentInput;
  name?: string;
  organization?: IOrganization;
}
