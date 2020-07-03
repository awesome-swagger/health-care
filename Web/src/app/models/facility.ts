import { MomentInput } from 'moment';

import { IHaveId } from './ihave-id';
import { IOrganization } from './organization';

export interface ISimpleFacility extends IHaveId {
  name?: string;
}

export interface IFacility extends ISimpleFacility{
  active_users?: number;
  addr_city?: string;
  addr_state?: string;
  addr_street?: string;
  addr_suite?: string;
  addr_zip?: string;
  created?: MomentInput;
  is_affiliate?: boolean;
  is_manager?: boolean;
  modified?: MomentInput;
  organization?: IOrganization;
  parent_company?: string;
}
