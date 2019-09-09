import { MomentInput } from "moment";

import { IHaveId } from "./ihaveid";
import { IOrganization } from "./organization";

export interface IFacility extends IHaveId {
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
  name?: string;
  organization?: IOrganization;
  parent_company?: string;
}
