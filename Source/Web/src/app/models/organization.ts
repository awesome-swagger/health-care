import { MomentInput } from 'moment';

import { IHaveId } from './ihave-id';

export interface IOrganization extends IHaveId {
        addr_city?: string;
       addr_state?: string;
      addr_street?: string;
       addr_suite?: string;
         addr_zip?: string;
  available_users?: number;
          created?: MomentInput;
       is_manager?: boolean;
         modified?: MomentInput;
             name?: string;
     renewal_date?: MomentInput;
}
